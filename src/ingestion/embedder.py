import json
from sentence_transformers import SentenceTransformer
from chunker import chunk_paper

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def get_model():
    """Load the model once and reuse it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts, batch_size=32):
    """Return one embedding (list of 384 numbers) per text."""
    vecs = get_model().encode(texts, batch_size=batch_size,
                              normalize_embeddings=True)
    return vecs.tolist()


if __name__ == "__main__":
    papers = json.load(open("data/processed/papers.json", encoding="utf-8"))
    chunks = [c for p in papers for c in chunk_paper(p)]
    vectors = embed_texts([c["text"] for c in chunks])
    print(len(vectors), "vectors of size", len(vectors[0]))