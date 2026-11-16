\# Ingestion



Fetches papers from ArXiv and PubMed and saves them in one common format.



\## Files

\- arxiv\_client.py: fetch\_arxiv\_papers(category, max\_results)

\- pubmed\_client.py: fetch\_pubmed\_papers(query, max\_results)

\- normalizer.py: removes incomplete papers and duplicates

\- scheduler.py: updates data/processed/papers.json every 6 hours



\## Run

python src\\ingestion\\scheduler.py



\## Notes

\- peer\_reviewed is true for PubMed, and for ArXiv only if journal\_ref exists.

\- Output: data/processed/papers.json

