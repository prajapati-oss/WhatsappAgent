from app.rag.embeddings import embedding_service
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.api.upload import router as upload_router
# Import routes
from app.api.webhook import router as webhook_router

from app.api.webhook import router as webhook_router
from app.rag.upload import router as upload_router
# ==============================
# Startup / Shutdown Events
# ==============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs during app startup and shutdown.
    Best place for:
    - DB connections
    - Redis connections
    - ML model loading
    - background workers
    """

    print("🚀 Starting WhatsApp AI Agent Server...")

    yield

    print("🛑 Shutting down server...")


# ==============================
# FastAPI App
# ==============================

app = FastAPI(
    title="WhatsApp AI Agent",
    description="Industry-grade WhatsApp AI Agent Backend",
    version="1.0.0",
    lifespan=lifespan
)


# ==============================
# CORS Middleware
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Include Routes
# ==============================
app.include_router(
    upload_router,
    prefix="/api"
)
app.include_router(
    webhook_router,
    prefix="/webhook"
)


app.include_router(
    webhook_router,
    prefix="/webhook",
    tags=["Webhook"]
)

app.include_router(
    upload_router,
    prefix="/api"
)

# ==============================
# Root Endpoint
# ==============================

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "WhatsApp AI Agent Running 🚀"
    }


# ==============================
# Health Check Endpoint
# ==============================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# ==============================
# Run Server
# ==============================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )