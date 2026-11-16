import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from arxiv_client import fetch_arxiv_papers
from pubmed_client import fetch_pubmed_papers
from normalizer import normalize

PATH = "data/processed/papers.json"


def load_existing():
    if os.path.exists(PATH):
        with open(PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def update_papers():
    existing = load_existing()
    known = {p["paper_id"] for p in existing}
    try:
        fresh = (fetch_arxiv_papers("cs.LG", 20)
                 + fetch_pubmed_papers("machine learning", 20))
    except Exception as e:
        print("fetch failed:", e)
        return
    new = [p for p in normalize(fresh) if p["paper_id"] not in known]
    os.makedirs("data/processed", exist_ok=True)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(existing + new, f, indent=2, ensure_ascii=False)
    print(f"{len(new)} new papers, {len(existing) + len(new)} total")


if __name__ == "__main__":
    update_papers()
    sched = BlockingScheduler()
    sched.add_job(update_papers, "interval", hours=6)
    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        print("Stopped")