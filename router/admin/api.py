from http.client import HTTPException
import shutil
from fastapi import APIRouter, Depends, File, UploadFile
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


@router.post("/upload/drawer_logo")
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


@router.post("/upload/carousel_images")
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


@router.post("/add/recipe")
async def add_recipe(recipe_data: RecipesCreate, category_id: int, thumbnail_file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_location = f"static/recipe_thumbnails/{thumbnail_file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(thumbnail_file.file, buffer)
        recipe_data.thumbnail = file_location
        
        recipe = Recipes(**recipe_data.dict(), category_id=category_id)
        
        if db.query(Recipes).filter(Recipes.title == recipe.title).first():
            raise HTTPException(status_code=400, detail="Recipe title already exists")
        
        category = db.query(Categories).filter(Categories.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        category.recipes.append(recipe)
        
        db.add(recipe)
        db.commit()
        db.refresh(recipe)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse(status_code=200, content={"message": "Recipe added successfully"})

