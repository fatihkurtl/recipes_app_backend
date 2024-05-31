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

