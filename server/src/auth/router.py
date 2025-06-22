from fastapi import APIRouter

from src.core.metadata import ApiTags

router = APIRouter(
    prefix='/auth',
    tags=[ApiTags.auth]
)

# TO-DO: Add authentication routes