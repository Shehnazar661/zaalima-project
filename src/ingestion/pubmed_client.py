import time
from Bio import Entrez

Entrez.email = "kmoshehnaz@gmail.com"  # NCBI requires an email


def fetch_pubmed_papers(query="machine learning", max_results=20):
    """Search PubMed, then fetch details for each paper found."""
    search = Entrez.read(Entrez.esearch(
        db="pubmed", term=query, retmax=max_results, sort="date"))
    ids = search["IdList"]
    if not ids:
        return []

    time.sleep(0.4)  # be polite to NCBI's rate limit
    records = Entrez.read(Entrez.efetch(
        db="pubmed", id=",".join(ids), retmode="xml"))

    papers = []
    for rec in records["PubmedArticle"]:
        cit = rec["MedlineCitation"]
        art = cit["Article"]
        pmid = str(cit["PMID"])

        parts = art.get("Abstract", {}).get("AbstractText", [])
        abstract = " ".join(str(p) for p in parts).strip()
        if not abstract:
            continue  # nothing to embed later, so skip

        authors = []
        for a in art.get("AuthorList", []):
            name = f"{a.get('ForeName', '')} {a.get('LastName', '')}".strip()
            if name:
                authors.append(name)

        if art.get("ArticleDate"):
            d = art["ArticleDate"][0]
            published = f"{d['Year']}-{d['Month']}-{d['Day']}"
        else:
            published = str(art["Journal"]["JournalIssue"]["PubDate"].get("Year", ""))

        papers.append({
            "paper_id": f"pubmed:{pmid}",
            "title": str(art["ArticleTitle"]).strip(),
            "abstract": abstract,
            "authors": authors,
            "published": published,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "pdf_url": None,
            "journal_ref": str(art["Journal"]["Title"]),
            "source": "pubmed",
            "peer_reviewed": True,
        })
    return papers


if __name__ == "__main__":
    for p in fetch_pubmed_papers("machine learning", 5):
        print(p["paper_id"], "|", p["published"], "|", p["peer_reviewed"], "|", p["title"][:50])