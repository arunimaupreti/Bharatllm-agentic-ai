from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


def _embed_texts(texts: List[str], model: SentenceTransformer) -> np.ndarray:
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.array(vectors).astype("float32")


def build_faiss_index(
    chunks_path: str,
    index_path: str,
    metadata_path: str,
    model_name: str = MODEL_NAME,
) -> None:
    if not Path(chunks_path).exists():
        raise FileNotFoundError(f"Chunks file not found: {chunks_path}")

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]
    metadata = [c["metadata"] for c in chunks]

    model = SentenceTransformer(model_name)
    embeddings = _embed_texts(texts, model)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    Path(metadata_path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, index_path)
    with open(metadata_path, "wb") as f:
        pickle.dump({"texts": texts, "metadata": metadata}, f)


def load_index_and_store(index_path: str, metadata_path: str) -> Tuple[faiss.Index, Dict]:
    index = faiss.read_index(index_path)
    with open(metadata_path, "rb") as f:
        store = pickle.load(f)
    return index, store


def embed_query(query: str, model: SentenceTransformer) -> np.ndarray:
    return _embed_texts([query], model)
