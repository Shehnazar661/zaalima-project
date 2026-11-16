import re
import arxiv


def fetch_arxiv_papers(category="cs.LG", max_results=20):
    """Fetch the newest papers from one ArXiv category."""
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    papers = []
    for r in arxiv.Client().results(search):
        short_id = re.sub(r"v\d+$", "", r.get_short_id())  # drop version, e.g. v1
        papers.append({
            "paper_id": f"arxiv:{short_id}",
            "title": r.title.strip(),
            "abstract": r.summary.strip().replace("\n", " "),
            "authors": [a.name for a in r.authors],
            "published": str(r.published.date()),
            "url": r.entry_id,
            "pdf_url": r.pdf_url,
            "journal_ref": r.journal_ref,
            "source": "arxiv",
            "peer_reviewed": r.journal_ref is not None,
        })
    return papers


if __name__ == "__main__":
    for p in fetch_arxiv_papers("cs.LG", 5):
        print(p["paper_id"], "|", p["published"], "|", p["peer_reviewed"], "|", p["title"][:50])