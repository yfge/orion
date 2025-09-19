from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .systems import router as systems_router
from .endpoints import router as endpoints_router
from .auth_profiles import router as auth_profiles_router
from .message_definitions import router as msg_defs_router
from .notify import router as notify_router


router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "pong"}


router.include_router(auth_router)
router.include_router(users_router)
router.include_router(systems_router)
router.include_router(endpoints_router)
router.include_router(auth_profiles_router)
router.include_router(msg_defs_router)
router.include_router(notify_router)
