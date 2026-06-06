import pickle
import time
import logging

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import config

logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(self):
        self.tfidf = None
        self.tfidf_matrix = None
        self.df: pd.DataFrame | None = None
        self._load_models()

    def _load_models(self):
        logger.info("Memuat model TF-IDF...")
        try:
            with open(config.TFIDF_VECTORIZER_PATH, "rb") as f:
                self.tfidf = pickle.load(f)
            with open(config.TFIDF_MATRIX_PATH, "rb") as f:
                self.tfidf_matrix = pickle.load(f)
            self.df = pd.read_pickle(config.GAMES_DF_PATH)
            logger.info(
                "Model berhasil dimuat. "
                "(%d games, %s)",
                len(self.df),
                str(self.tfidf_matrix.shape),
            )
        except Exception as e:
            logger.error("Gagal load model: %s: %s", type(e).__name__, e)
            self.tfidf = None
            self.tfidf_matrix = None
            self.df = None

    @property
    def models_loaded(self) -> bool:
        return (
            self.tfidf is not None
            and self.tfidf_matrix is not None
            and self.df is not None
        )

    def recommend(self, query: str, top_n: int = 5) -> dict:
        start = time.perf_counter()

        query_vec = self.tfidf.transform([query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = sim_scores.argsort()[::-1][:top_n]

        results = self.df.iloc[top_indices][
            ["title", "rating", "desc_sentence", "tags_clean"]
        ].copy()
        results["similarity_score"] = np.round(sim_scores[top_indices], 4)
        results = results.reset_index(drop=True)

        latency = round((time.perf_counter() - start) * 1000, 2)

        return {
            "query": query,
            "recommendations": results.to_dict("records"),
            "meta": {"latency_ms": latency},
        }
