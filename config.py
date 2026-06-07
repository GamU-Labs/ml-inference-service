import os
from dotenv import load_dotenv

load_dotenv()


PORT = int(os.getenv("ML_INFERENCE_PORT", "8998"))
DEBUG = os.getenv("ML_INFERENCE_DEBUG", "false").lower() == "true"

MODEL_DIR = os.getenv("MODEL_DIR", "models")
TFIDF_VECTORIZER_PATH = os.getenv(
    "TFIDF_VECTORIZER_PATH",
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"),
)
TFIDF_MATRIX_PATH = os.getenv(
    "TFIDF_MATRIX_PATH",
    os.path.join(MODEL_DIR, "tfidf_matrix.pkl"),
)
GAMES_DF_PATH = os.getenv(
    "GAMES_DF_PATH",
    os.path.join(MODEL_DIR, "clean_games_df.pkl"),
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
