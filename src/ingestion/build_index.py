import json
import os
from arxiv_client import fetch_arxiv_papers
from pubmed_client import fetch_pubmed_papers
from normalizer import normalize
from scheduler import load_existing, PATH
from chunker import chunk_paper
from vector_store import init_collection, upsert_chunks


def grow(n=100):
    """Fetch more papers and merge them into papers.json without duplicates."""
    existing = load_existing()
    known = {p["paper_id"] for p in existing}
    fresh = []
    for cat in ["cs.LG", "cs.AI", "cs.CL"]:
        fresh += fetch_arxiv_papers(cat, n)
    fresh += fetch_pubmed_papers("machine learning", n)
    new = [p for p in normalize(fresh) if p["paper_id"] not in known]
    papers = existing + new
    os.makedirs("data/processed", exist_ok=True)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    print(len(new), "new papers,", len(papers), "total")
    return papers


if __name__ == "__main__":
    papers = grow(100)
    chunks = [c for p in papers for c in chunk_paper(p)]
    init_collection()
    print(upsert_chunks(chunks), "chunks in vector DB")