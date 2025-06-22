from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan for a fastapi application.

    Args:
        app: Instantiated fastapi application.
    """
    logger.info('Starting FastAPI application...')
    yield
    logger.info('Closing FastAPI application...')
