import json
from pymilvus import MilvusClient
from chunker import chunk_paper
from embedder import embed_texts

DB_PATH = "data/vectors.db"
COLLECTION = "papers"
DIM = 384
META = ["paper_id", "title", "source", "peer_reviewed", "published", "url", "text"]
_client = None


def get_client():
    global _client
    if _client is None:
        _client = MilvusClient(DB_PATH)
        if _client.has_collection(COLLECTION):
            _client.load_collection(COLLECTION)
    return _client 


def init_collection():
    c = get_client()
    if not c.has_collection(COLLECTION):
        c.create_collection(
            collection_name=COLLECTION, dimension=DIM,
            primary_field_name="id", id_type="string", max_length=200,
            vector_field_name="vector", metric_type="COSINE", auto_id=False)


def upsert_chunks(chunks):
    """Embed chunks and store them. Re-running never creates duplicates."""
    vectors = embed_texts([c["text"] for c in chunks])
    rows = [{"id": c["chunk_id"], "vector": v, **{k: c[k] for k in META}}
            for c, v in zip(chunks, vectors)]
    get_client().upsert(COLLECTION, rows)
    return len(rows)


def search(query_vector, k=5, peer_reviewed_only=False):
    def search(query_vector, k=5, peer_reviewed_only=False):
        get_client().load_collection(COLLECTION)
    flt = "peer_reviewed == true" if peer_reviewed_only else ""
    flt = "peer_reviewed == true" if peer_reviewed_only else ""
    res = get_client().search(
        COLLECTION, data=[query_vector], limit=k, filter=flt,
        output_fields=META)
    return res[0]


if __name__ == "__main__":
    papers = json.load(open("data/processed/papers.json", encoding="utf-8"))
    chunks = [c for p in papers for c in chunk_paper(p)]
    init_collection()
    print(upsert_chunks(chunks), "chunks stored")

    q = embed_texts(["machine learning for disease prediction"])[0]
    for label, only in [("all", False), ("peer reviewed only", True)]:
        print("---", label)
        for r in search(q, 3, only):
            e = r["entity"]
            print(round(r["distance"], 3), e["peer_reviewed"], e["title"][:50])