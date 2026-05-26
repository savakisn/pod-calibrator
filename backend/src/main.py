from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from .routes.import_deck import analyze_from_url
from .routes.export import generate_export_jpeg

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/import", methods=["POST"])
def import_deck():
    try:
        data = request.get_json()
        url = data.get("url", "")
        result = analyze_from_url(url)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to fetch deck: {str(e)}"}), 502

@app.route("/api/export", methods=["POST"])
def export_card():
    try:
        data = request.get_json()
        analysis = data.get("analysis")
        if not analysis:
            return jsonify({"error": "No analysis provided"}), 400

        color_mode = data.get("colorMode", "default")
        jpeg_io = generate_export_jpeg(analysis, color_mode)
        commander_name = analysis.get('commander', {}).get('name', 'deck').replace(' ', '-').lower()
        filename = f"{commander_name}-pod-calibrator.jpg"

        return send_file(jpeg_io, mimetype='image/jpeg', as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
