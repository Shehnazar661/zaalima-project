import json
import os
from retriever import retrieve
from prompt_builder import build_rag_prompt

QUESTION = "How is machine learning used for disease prediction?"

papers = json.load(open("data/processed/papers.json", encoding="utf-8"))
pr = sum(p["peer_reviewed"] for p in papers)
print(f"1) INGESTION: {len(papers)} papers ({pr} peer-reviewed, "
      f"{len(papers) - pr} preprints) from ArXiv + PubMed")

print("\n2) SEARCH (peer-reviewed only):")
chunks = retrieve(QUESTION, 3, {"peer_reviewed": True})
for c in chunks:
    print(f"  {c['score']}  [{c['chunk_id']}]  {c['title'][:55]}")

print("\n3) RAG PROMPT (first 600 chars):")
prompt = build_rag_prompt(QUESTION, chunks)
print(prompt[:600], "...")

key = os.environ.get("ANTHROPIC_API_KEY")
if key:
    import anthropic
    reply = anthropic.Anthropic(api_key=key).messages.create(
        model="claude-sonnet-5-5", max_tokens=500,
        messages=[{"role": "user", "content": prompt}])
    print("\n4) ANSWER:\n", reply.content[0].text)
else:
    print("\n4) ANSWER: skipped (no ANTHROPIC_API_KEY set)")
open("data/last_prompt.txt", "w", encoding="utf-8").write(prompt)
print("\nFull prompt saved to data/last_prompt.txt")