from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .systems import router as systems_router


router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "pong"}


router.include_router(auth_router)
router.include_router(users_router)
router.include_router(systems_router)
