from fastapi import APIRouter

from .api_keys import router as api_keys_router
from .auth import router as auth_router
from .auth_profiles import router as auth_profiles_router
from .endpoints import router as endpoints_router
from .message_definitions import router as msg_defs_router
from .notify import router as notify_router
from .schema import router as schema_router
from .send_records import router as send_records_router
from .systems import router as systems_router
from .users import router as users_router

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
router.include_router(schema_router)
router.include_router(send_records_router)
router.include_router(api_keys_router)
