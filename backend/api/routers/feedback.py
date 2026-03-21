from fastapi import APIRouter
from pydantic import BaseModel
from feedback.store import save_feedback, init_db
from feedback.trainer import retrain_from_feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])

class FeedbackRequest(BaseModel):
    query: str
    sql_used: str
    rating: int        # 1 = thumbs up, -1 = thumbs down
    comment: str = ""

@router.post("/")
async def submit_feedback(req: FeedbackRequest):
    if req.rating not in (1, -1):
        return {"status": "error", "message": "rating must be 1 or -1"}
    fid = save_feedback(req.query, req.sql_used, req.rating, req.comment)
    # Attempt retraining if we have enough positive feedback
    retrain_result = retrain_from_feedback(min_samples=10)
    return {
        "status": "saved",
        "feedback_id": fid,
        "retrain": retrain_result,
    }
