import os
import sys

# let this folder import the ingestion modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingestion"))

from embedder import embed_texts  # noqa: E402
from vector_store import search  # noqa: E402


def retrieve(query, k=5, filters=None):
    """Return the k most relevant chunks as RetrievedChunk dicts.

    filters example: {"peer_reviewed": True}
    """
    filters = filters or {}
    vec = embed_texts([query])[0]
    hits = search(vec, k, peer_reviewed_only=bool(filters.get("peer_reviewed")))
    results = []
    for h in hits:
        e = h["entity"]
        results.append({
            "chunk_id": h["id"],
            "paper_id": e["paper_id"],
            "title": e["title"],
            "source": e["source"],
            "peer_reviewed": e["peer_reviewed"],
            "published": e["published"],
            "text": e["text"],
            "score": round(h["distance"], 3),
            "url": e["url"],
        })
    return results


if __name__ == "__main__":
    q = "neural network training"
    for label, f in [("no filter", None), ("peer reviewed only", {"peer_reviewed": True})]:
        print("---", label)
        for r in retrieve(q, 4, f):
            print(r["score"], r["source"], r["peer_reviewed"], r["title"][:45])