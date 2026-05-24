import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from .routes.analyze import analyze_deck_sync
from .routes.import_deck import analyze_from_moxfield

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        decklist = data.get("decklist", "")
        result = analyze_deck_sync(decklist)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/import/moxfield", methods=["POST"])
def import_moxfield():
    try:
        data = request.get_json()
        url = data.get("url", "")
        result = analyze_from_moxfield(url)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to fetch deck: {str(e)}"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
