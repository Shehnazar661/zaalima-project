def build_rag_prompt(question, chunks):
    """Build a prompt that forces answers to stay inside the retrieved text."""
    if not chunks:
        context = "(no relevant papers found)"
    else:
        context = "\n\n".join(
            f"[{c['chunk_id']}] ({c['source']}, "
            f"{'peer-reviewed' if c['peer_reviewed'] else 'preprint'}, "
            f"{c['published']}) {c['title']}\n{c['text']}"
            for c in chunks)

    return (
        "You are a careful research assistant.\n"
        "Answer the question using ONLY the context below.\n"
        "After every claim, cite the chunk id in square brackets, "
        "for example [arxiv:2611.18563#c0].\n"
        "If the context does not contain the answer, reply exactly: "
        "\"The provided papers do not answer this.\"\n"
        "Do not use outside knowledge.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\nANSWER:"
    )


if __name__ == "__main__":
    from retriever import retrieve

    q = "machine learning for disease prediction"
    prompt = build_rag_prompt(q, retrieve(q, 3, {"peer_reviewed": True}))
    print(prompt[:1500])