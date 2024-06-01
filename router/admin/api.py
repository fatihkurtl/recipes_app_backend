from http.client import HTTPException
import os
import shutil
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import AppImages, Recipes, Categories
from .admin_auth import authenticate_admin, create_admin, create_admin_contact
from schemas.admin_schema import LoginData, RegisterData, AdminContactData
from schemas.app_schema import RecipesBase, CategoriesBase, RecipesCreate

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},    
)

@router.post("/api/register")
async def register_admin(register_data: RegisterData, db: Session = Depends(get_db)):
    return create_admin(db, register_data.fullname, register_data.username, register_data.email, register_data.password)
    

@router.post("/api/login")
async def login_admin(login_data: LoginData, db: Session = Depends(get_db)):
    return authenticate_admin(db, login_data.email, login_data.password)


@router.post("/api/contact")
async def contact_admin(contact_data: AdminContactData, db: Session = Depends(get_db)):
    return create_admin_contact(db, contact_data.email, contact_data.subject, contact_data.message)


@router.post("/api/upload/drawer_logo")
async def upload_drawer_logo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_location = f"static/drawer_logo/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        app_images = db.query(AppImages).first()
        if not app_images:
            app_images = AppImages()
        app_images.drawer_header_logo = file_location
        db.add(app_images)
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse(status_code=200, content={"message": "Drawer logo uploaded successfully"})


@router.post("/api/upload/carousel_images")
async def upload_carousel_images(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    try:
        file_locations = []
        for file in files:
            file_location = f"static/carousel_images/{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_locations.append(file_location)
        
        app_images = db.query(AppImages).first()
        if not app_images:
            app_images = AppImages()
        for file_location in file_locations:
            app_images.add_carousel_image(file_location)
        db.add(app_images)
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse(status_code=200, content={"message": "Carousel images uploaded successfully"})


@router.post("/api/add/recipe")
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
    try:
        filename, file_extension = os.path.splitext(thumbnail.filename)
        file_location = f"static/recipe_thumbnails/{thumbnail.filename}"
        print("File Location:", file_location)
        
        # Klasörü oluştur
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(thumbnail.file, buffer)

        category = db.query(Categories).filter(Categories.category_name == category_name).first()
        if not category:
            category = Categories(category_name=category_name, category_name_en=category_name_en)
            db.add(category)
            db.commit()
            db.refresh(category)

        recipe = Recipes(title=title, 
                         title_en=title_en, 
                         description=description, 
                         description_en=description_en, 
                         thumbnail_file=file_location, 
                         save_count=save_count, 
                         popular=popular, 
                         active=active, 
                         category_id=category.id)

        if db.query(Recipes).filter(Recipes.title == recipe.title).first():
            raise HTTPException(status_code=400, detail="Recipe title already exists")

        db.add(recipe)
        db.commit()
        db.refresh(recipe)
    except FileNotFoundError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    return JSONResponse(status_code=200, content={"message": "Recipe added successfully"})


