import json
import os
from arxiv_client import fetch_arxiv_papers
from pubmed_client import fetch_pubmed_papers

REQUIRED = ["paper_id", "title", "abstract", "authors", "published",
            "url", "pdf_url", "journal_ref", "source", "peer_reviewed"]


def normalize(papers):
    """Keep only complete papers and drop duplicates by paper_id."""
    clean = {}
    for p in papers:
        if any(k not in p for k in REQUIRED) or not p["abstract"]:
            continue
        clean[p["paper_id"]] = p
    return list(clean.values())


def collect(arxiv_cat="cs.LG", pubmed_query="machine learning", n=20):
    papers = fetch_arxiv_papers(arxiv_cat, n) + fetch_pubmed_papers(pubmed_query, n)
    papers = normalize(papers)
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/papers.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    return papers


if __name__ == "__main__":
    papers = collect(n=10)
    print(len(papers), "papers saved")
    print("peer reviewed:", sum(p["peer_reviewed"] for p in papers))