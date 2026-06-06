import logging

from flask import Flask, request, jsonify

import config
from lib.response import respond_success, respond_error
from services.inference import InferenceService

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
inference = InferenceService()

SERVICE_NAME = "ml-inference-service"
SERVICE_VERSION = "0.1.0"


@app.route("/api/v1", methods=["GET"])
def index():
    return respond_success({
        "name": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "status": "ok",
    })


@app.route("/api/v1/health", methods=["GET"])
def health():
    return respond_success({
        "status": "ok",
        "models_loaded": inference.models_loaded,
    })


@app.route("/api/v1/recommend", methods=["POST"])
def recommend():
    if not inference.models_loaded:
        return respond_error(
            message="Model belum dimuat. Periksa file model.",
            error="ModelNotLoadedError",
            status=503,
        )

    body = request.get_json(silent=True)
    if not body:
        return respond_error(
            message="Request body harus berupa JSON.",
            error="ValidationError",
            status=400,
        )

    query = (body.get("query") or "").strip()
    if not query:
        return respond_error(
            message="Field 'query' wajib diisi.",
            error="ValidationError",
            status=400,
        )
    if len(query) > 500:
        return respond_error(
            message="Panjang 'query' maksimal 500 karakter.",
            error="ValidationError",
            details={"max_length": 500},
            status=400,
        )

    try:
        top_n = int(body.get("top_n", 5))
    except (TypeError, ValueError):
        return respond_error(
            message="Field 'top_n' harus berupa angka.",
            error="ValidationError",
            status=400,
        )

    if top_n < 1 or top_n > 20:
        return respond_error(
            message="Nilai 'top_n' harus antara 1–20.",
            error="ValidationError",
            details={"min": 1, "max": 20},
            status=400,
        )

    try:
        result = inference.recommend(query, top_n=top_n)
    except Exception as e:
        logger.exception("TF-IDF inference gagal")
        return respond_error(
            message=f"Inference gagal: {e}",
            error="InferenceError",
            status=500,
        )

    return respond_success(result)


if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT)
