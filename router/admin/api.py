from http.client import HTTPException
import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import AppImages, Recipes, Categories
from models.members import Members
from router.admin.admin_crud import get_all_members, get_create_recipe, get_upload_carouesel_images, get_upload_drawer_logo
from schemas.members_schema import Member
from .admin_auth import authenticate_admin, create_admin, create_admin_contact
from schemas.admin_schema import LoginData, RegisterData, AdminContactData
from schemas.app_schema import RecipesBase, CategoriesBase, RecipesCreate

router = APIRouter(
    prefix="/admin/api",
    tags=["admin"],
    responses={404: {"description": "Not found"}},    
)

@router.post("/register")
async def register_admin(register_data: RegisterData, db: Session = Depends(get_db)):
    return create_admin(db, register_data.fullname, register_data.username, register_data.email, register_data.password)
    

@router.post("/login")
async def login_admin(login_data: LoginData, db: Session = Depends(get_db)):
    return authenticate_admin(db, login_data.email, login_data.password)


@router.post("/contact")
async def contact_admin(contact_data: AdminContactData, db: Session = Depends(get_db)):
    return create_admin_contact(db, contact_data.email, contact_data.subject, contact_data.message)


@router.post("/upload/drawer_logo")
async def upload_drawer_logo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return get_upload_drawer_logo(file, db)


@router.post("/upload/carousel_images")
async def upload_carousel_images(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    return get_upload_carouesel_images(files, db)


@router.post("/add/recipe")
async def add_recipe(title: str = Form(...), 
                     title_en: str = Form(...), 
                     description: str = Form(...), 
                     description_en: str = Form(...), 
                     thumbnail: UploadFile = File(...), 
                     save_count: int = Form(0), 
                     popular: bool = Form(False), 
                     active: bool = Form(True), 
                     category_name: str = Form(...), 
                     category_name_en: str = Form(...), 
                     db: Session = Depends(get_db)):
    return get_create_recipe(db, title, title_en, description, description_en, thumbnail, save_count, popular, active, category_name, category_name_en)


@router.get("/all/members", response_model=List[Member])
async def get_members(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_all_members(db, skip, limit)
    
