from fastapi import FastAPI
from typing import Union

from dotenv import load_dotenv
from router.admin import api as admin_login
from router.app import api as app_api
from database.db import Base, engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(admin_login.router)

app.include_router(app_api.router)