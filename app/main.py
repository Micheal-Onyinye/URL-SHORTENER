from fastapi import FastAPI
from app.routes import url_route

app = FastAPI()

app.include_router(url_route.router)
