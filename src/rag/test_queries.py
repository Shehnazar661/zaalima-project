from retriever import retrieve

QUERIES = [
    "machine learning for disease prediction",
    "large language model evaluation",
    "neural network training",
    "deep learning in medical imaging",
    "bias in machine learning models",
    "cancer prognosis prediction",
    "reinforcement learning",
    "contrastive representation learning",
    "stroke treatment outcomes",
    "agriculture and artificial intelligence",
]

for q in QUERIES:
    print("\nQ:", q)
    for r in retrieve(q, 3):
        print("  ", r["score"], r["source"], "|", r["title"][:55])