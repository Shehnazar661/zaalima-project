import json


def chunk_text(text, size=400, overlap=60):
    """Split text into word chunks of about `size` words with overlap."""
    words = text.split()
    if not words:
        return []
    chunks, start = [], 0
    while start < len(words):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
        start += size - overlap
    return chunks


def chunk_paper(paper):
    """Turn one paper into chunk records that keep the paper's metadata."""
    body = paper["title"] + ". " + paper["abstract"]
    return [{
        "chunk_id": f"{paper['paper_id']}#c{i}",
        "paper_id": paper["paper_id"],
        "title": paper["title"],
        "source": paper["source"],
        "peer_reviewed": paper["peer_reviewed"],
        "published": paper["published"],
        "url": paper["url"],
        "text": text,
    } for i, text in enumerate(chunk_text(body))]


if __name__ == "__main__":
    papers = json.load(open("data/processed/papers.json", encoding="utf-8"))
    chunks = [c for p in papers for c in chunk_paper(p)]
    print(len(papers), "papers ->", len(chunks), "chunks")
    print(chunks[0]["chunk_id"], "|", chunks[0]["text"][:100])