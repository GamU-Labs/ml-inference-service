import logging

from flask import Flask, request, jsonify

import config
from services.inference import InferenceService

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
inference = InferenceService()


def respond_success(data: dict, status: int = 200):
    return jsonify({"data": data}), status


def respond_error(message: str, status: int = 400):
    return jsonify({"message": message}), status


@app.route("/health", methods=["GET"])
def health():
    return respond_success({
        "status": "ok",
        "models_loaded": inference.models_loaded,
    })


@app.route("/ml/recommend", methods=["POST"])
def recommend():
    if not inference.models_loaded:
        return respond_error(
            "Model belum dimuat. Periksa file model.", 503
        )

    body = request.get_json(silent=True)
    if not body:
        return respond_error("Request body harus berupa JSON.", 400)

    query = (body.get("query") or "").strip()
    if not query:
        return respond_error("Field 'query' wajib diisi.", 400)
    if len(query) < 1 or len(query) > 500:
        return respond_error("Panjang 'query' harus 1–500 karakter.", 400)

    try:
        top_n = int(body.get("top_n", 5))
    except (TypeError, ValueError):
        return respond_error("Field 'top_n' harus berupa angka.", 400)

    if top_n < 1 or top_n > 20:
        return respond_error("Nilai 'top_n' harus antara 1–20.", 400)

    try:
        result = inference.recommend(query, top_n=top_n)
    except Exception as e:
        logger.exception("TF-IDF inference gagal")
        return respond_error(f"Inference gagal: {e}", 500)

    return respond_success(result)


if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT)
