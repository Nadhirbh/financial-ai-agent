from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.chatbot import router as chatbot_router
from .api.v1.health import router as health_router
from .api.v1.analytics import router as analytics_router
from .api.v1.ingest import router as ingest_router
from .api.v1.nlp import router as nlp_router
from .api.v1.insights import router as insights_router
from .db.models import Base
from .db.session import engine

app = FastAPI(title="Financial AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(chatbot_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(ingest_router, prefix="/api/v1")
app.include_router(nlp_router, prefix="/api/v1")
app.include_router(insights_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "ok", "service": "financial-ai-agent"}


@app.on_event("startup")
def on_startup():
    # Ensure DB tables exist (dev convenience)
    Base.metadata.create_all(bind=engine)
