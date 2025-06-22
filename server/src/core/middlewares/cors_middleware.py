from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings

def add(app: FastAPI) -> None:
    """
    Adds Cors middleware to the application.

    Args:
        app: Instantiated FastAPI application. 

    Returns:
        None
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )