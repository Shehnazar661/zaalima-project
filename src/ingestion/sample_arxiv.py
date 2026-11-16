import arxiv, json

search = arxiv.Search(query="cat:cs.LG", max_results=5,
                      sort_by=arxiv.SortCriterion.SubmittedDate)
papers = []
for r in arxiv.Client().results(search):
    papers.append({"id": r.get_short_id(), "title": r.title,
                   "abstract": r.summary, "published": str(r.published.date()),
                   "pdf": r.pdf_url, "journal_ref": r.journal_ref})
json.dump(papers, open("data/raw/sample_arxiv.json", "w"), indent=2)
print(len(papers), "saved")