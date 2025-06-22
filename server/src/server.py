from fastapi import FastAPI

from src.core.lifespan import lifespan
from src.core.middlewares import cors_middleware
from src.user.router import router as user_router
from src.auth.router import router as auth_router
from src.core.metadata import title, version, description, tags

api = FastAPI(
    title=title,
    version=version,
    description=description,
    openapi_tags=tags,
    lifespan=lifespan
)

cors_middleware.add(api)

api.include_router(auth_router)
api.include_router(user_router)