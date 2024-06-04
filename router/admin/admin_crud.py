import os
import shutil
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models.app import AppImages, Categories, Recipes
from models.members import Members
from schemas.members_schema import MemberBase



def get_create_recipe(db: Session, title: str, title_en: str, description: str, description_en: str, thumbnail: UploadFile, save_count: int, popular: bool, active: bool, category_name: str, category_name_en: str):
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


def get_upload_carouesel_images(files: list[UploadFile], db: Session):
    try:
        file_locations = []
        for file in files:
            file_location = f"static/carousel_images/{file.filename}"
            
            os.makedirs(os.path.dirname(file_location), exist_ok=True)

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


def get_upload_drawer_logo(file: UploadFile, db: Session):
    try:
        file_location = f"static/drawer_logo/{file.filename}"
        
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

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


def get_all_members(db: Session, skip: int = 0, limit: int = 10):
    try:
        members = db.query(Members).offset(skip).limit(limit).all()
        if not members:
            raise HTTPException(status_code=404, detail="No members found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return [MemberBase.from_orm(member) for member in members]