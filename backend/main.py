from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.query import router as query_router
from api.routers.feedback import router as feedback_router
from core.vanna_bridge import train_if_needed

app = FastAPI(
    title="MDM RAG System",
    description="Meter Data Management with RAG and Streaming",
    version="2.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)
app.include_router(feedback_router)

@app.on_event("startup")
async def startup():
    # Attempt to train Vanna memory if not trained
    train_if_needed()

@app.get("/")
def root():
    return {
        "message": "MDM RAG System API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
