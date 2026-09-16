from fastapi import FastAPI

from app.api.v1.router import router

app = FastAPI(
    title="Computational API",
    version="1.0.0",
)

app.include_router(
    router,
    prefix="/api/v1",
)