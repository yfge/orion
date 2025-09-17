from fastapi import FastAPI

from .api.v1.router import router as api_v1_router


def create_app() -> FastAPI:
    app = FastAPI(title="Orion Notification Gateway", version="0.1.0")

    # Routers
    app.include_router(api_v1_router, prefix="/api/v1")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()

