from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings

app = FastAPI(title="Design Review API")

# CORS - required for Figma plugin (null origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache
def get_settings():
    return Settings()

@app.get("/health")
async def health():
    return {"status": "ok"}
