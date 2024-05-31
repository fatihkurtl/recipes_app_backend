from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import AppImages, Recipes, Categories
import os
import shutil
from schemas.app_schema import DrawerHeaderLogo, CarouselImages


router = APIRouter(
    prefix="/app",
    tags=["app"],
    responses={404: {"description": "Not found"}},
)




