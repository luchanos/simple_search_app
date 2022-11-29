import asyncpg
import uvicorn
from fastapi import FastAPI, Request
from elasticsearch import AsyncElasticsearch

from fastapi.routing import APIRoute, APIRouter

from handlers import create_document, ping
import settings


class Database():
    async def create_pool(self):
        self.pool = await asyncpg.create_pool(dsn=settings.POSTGRES_DATABASE_URL)


def create_app():
    app = FastAPI()
    db = Database()
    elastic = AsyncElasticsearch(settings.ELASTIC_URL)
    app.state.db = db
    app.state.elastic = elastic

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.pgpool = db.pool
        response = await call_next(request)
        return response

    @app.on_event("startup")
    async def startup():
        await db.create_pool()

    @app.on_event("shutdown")
    async def shutdown():
        await db.pool.close()

    return app


app = create_app()

routes = [
    APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
    APIRoute(path="/create_document", endpoint=create_document, methods=["POST"]),
]

app.include_router(APIRouter(routes=routes))


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
