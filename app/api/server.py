from fastapi import FastAPI
from app.api.routes import router

def create_app():
    app = FastAPI(
        title="LangGraph Observer",
        version="0.1.0",
    )

    app.include_router(router)

    return app

app = create_app()