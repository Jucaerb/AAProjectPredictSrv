from fastapi import FastAPI # type: ignore
from app.api import clustering
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

app.include_router(clustering.router, prefix="/api/clustering", tags=["Clustering"])
