from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncAzureOpenAI
from .config import Settings
from .routers import review, comments


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize AsyncAzureOpenAI client at startup."""
    settings = Settings()
    app.state.openai_client = AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
    )
    app.state.settings = settings
    yield
    # Shutdown: client closes automatically


app = FastAPI(title="Design Review API", lifespan=lifespan)

# CORS - required for Figma plugin (null origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review.router)
app.include_router(comments.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
