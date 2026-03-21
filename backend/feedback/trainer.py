"""
Periodically (or on-demand) retrain Vanna using thumbs-up feedback.
Good SQL from real user queries is the best training data.
"""
from core.vanna_client import get_vanna
from .store import get_positive_feedback, mark_retrained

def retrain_from_feedback(min_samples: int = 5) -> dict:
    """
    Use positive feedback to retrain Vanna.
    Only runs when we have enough samples.
    Returns {trained: bool, count: int}
    """
    samples = get_positive_feedback(limit=100)

    if len(samples) < min_samples:
        return {"trained": False, "count": len(samples),
                "message": f"Need {min_samples} samples, have {len(samples)}"}

    vn = get_vanna()
    trained_ids = []

    for s in samples:
        try:
            vn.agent_memory.add_sql(question=s["query"], sql=s["sql"])
            trained_ids.append(s["id"])
        except Exception as e:
            print(f"Failed to train on sample {s['id']}: {e}")

    if trained_ids:
        mark_retrained(trained_ids)
    return {"trained": True, "count": len(trained_ids)}
