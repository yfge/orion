from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import router as api_v1_router
from .core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Orion Notification Gateway", version="0.1.0")

    # CORS
    origins = settings.CORS_ORIGINS or [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_v1_router, prefix="/api/v1")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()
