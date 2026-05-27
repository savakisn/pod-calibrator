import logging
import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from .routes.import_deck import analyze_from_url, DeckImportError
from .routes.export import generate_export_jpeg, generate_comparison_jpeg, generate_comparison_table_jpeg

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger("pod-calibrator")

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/import", methods=["POST"])
def import_deck():
    started = time.monotonic()
    url = ""
    try:
        data = request.get_json() or {}
        url = (data.get("url") or "").strip()
        if not url:
            return jsonify({"error": "No URL provided."}), 400
        result, cache_hit = analyze_from_url(url)
        ms = int((time.monotonic() - started) * 1000)
        logger.info("import url=%s cache_hit=%s ms=%d", url, cache_hit, ms)
        result["_meta"] = {"cache_hit": cache_hit, "ms": ms}
        return jsonify(result)
    except DeckImportError as e:
        ms = int((time.monotonic() - started) * 1000)
        logger.warning("import_failed url=%s status=%d ms=%d msg=%s", url, e.status_code, ms, e)
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        ms = int((time.monotonic() - started) * 1000)
        logger.exception("import_error url=%s ms=%d", url, ms)
        return jsonify({"error": "Something went wrong. Try again in a moment."}), 502

@app.route("/api/export", methods=["POST"])
def export_card():
    try:
        data = request.get_json()
        analysis = data.get("analysis")
        if not analysis:
            return jsonify({"error": "No analysis provided"}), 400

        color_mode = data.get("colorMode", "deuteranopia")
        jpeg_io = generate_export_jpeg(analysis, color_mode)
        commander_name = analysis.get('commander', {}).get('name', 'deck').replace(' ', '-').lower()
        filename = f"{commander_name}-pod-calibrator.jpg"

        return send_file(jpeg_io, mimetype='image/jpeg', as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route("/api/export/comparison", methods=["POST"])
def export_comparison():
    try:
        data = request.get_json()
        analyses = data.get("analyses")
        if not analyses or len(analyses) < 2:
            return jsonify({"error": "At least 2 analyses required"}), 400

        color_mode = data.get("colorMode", "deuteranopia")
        jpeg_io = generate_comparison_jpeg(analyses, color_mode)

        return send_file(jpeg_io, mimetype='image/jpeg', as_attachment=True, download_name='pod-comparison.jpg')
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route("/api/export/table", methods=["POST"])
def export_table():
    try:
        data = request.get_json()
        analyses = data.get("analyses")
        if not analyses or len(analyses) < 2:
            return jsonify({"error": "At least 2 analyses required"}), 400

        color_mode = data.get("colorMode", "deuteranopia")
        jpeg_io = generate_comparison_table_jpeg(analyses, color_mode)

        return send_file(jpeg_io, mimetype='image/jpeg', as_attachment=True, download_name='pod-comparison-table.jpg')
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
