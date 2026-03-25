import contextlib
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import src.routers.system as system_router
import src.routers.analyze as analyze_router
from src.core.agent import agent
from src.models.settings import app_settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    logger = logging.getLogger("vertex")
    logger.info("🚀 Starting Vertex AI Agent...")

    if app_settings.qwen_api_key and app_settings.qwen_api_url:
        agent.set_config(app_settings.qwen_api_key, app_settings.qwen_api_url)
        logger.info("✅ AI Agent configured")
    else:
        logger.warning("⚠️ AI Agent not configured - check QWEN_API_KEY and QWEN_API_URL")

    yield
    logger.info("🛑 Vertex shutdown")


app = FastAPI(
    title="Vertex",
    version="0.1.0",
    description="AI-агент для анализа финансовой отчетности",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router.router)
app.include_router(analyze_router.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "Vertex AI"}
@app.get("/health")
async def root_health():
    """Health check на корневом пути"""
    return {"status": "ok", "service": "Vertex AI"}

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "service": "Vertex AI",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }