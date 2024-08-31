import logging

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from routes import api
from config.config import settings

def init_app():
    
    description = """
        This is a service for MESER COFFEE.
    """

    app = FastAPI(title="MESER COFFEE",
        description=description,
        version="2.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json")

    @app.on_event("startup")
    async def startup():
        pass
        # await init_db()
        
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    # app.add_middleware(ContextMiddleware)
    app.add_middleware(
    SQLAlchemyMiddleware,
        db_url=settings.DATABASE_URL,
        engine_args={
            "echo": False,
            "pool_pre_ping": True,
            "pool_recycle": 1800
        },
    )
    
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.backend_cors_origins,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api.api_router, prefix="/mesercoffee")
    add_pagination(app)

    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

    fastapi_logger.handlers = gunicorn_error_logger.handlers

    if __name__ != "__main__":
        fastapi_logger.setLevel(gunicorn_logger.level)
    else:
        fastapi_logger.setLevel(logging.DEBUG)

    return app

app = init_app()
