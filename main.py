from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from typing import Union

from dotenv import load_dotenv
from router.admin import api as admin_routes
from router.app import api as app_api
from database.db import Base, engine, get_db
from middlewares.cors import add_cors

app = FastAPI()

add_cors(app)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(admin_routes.router)

app.include_router(app_api.router)