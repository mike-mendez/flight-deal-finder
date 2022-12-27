from fastapi import APIRouter

from .endpoints import auth, users, utils, test

api_router = APIRouter()
# api_router.include_router(auth.router, tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(test.router, prefix="/tests", tags=["tests"])
