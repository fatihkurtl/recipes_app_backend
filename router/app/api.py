from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import all_
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import AppImages, Recipes, Categories
from schemas.app_schema import CategoriesBase, CategoriesInDBBase, RecipesBase, RecipesInDBBase
from .app_helpers import all_categories

router = APIRouter(
    prefix="/app/api",
    tags=["app"],
    responses={404: {"description": "Not found"}},
)


@router.get("/recipes/categories", response_model=CategoriesInDBBase)
async def categories(db: Session = Depends(get_db)):
    categories = all_categories(db)
    return {"categories": categories}


@router.get("/recipes/", response_model=List[RecipesBase])
async def get_recipes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    recipes = db.query(Recipes).offset(skip).limit(limit).all()
    return recipes


# @router.get("/recipes/{category}", response_model=RecipesInDBBase)
# async def get_recipes_by_category(category: str, db: Session = Depends(get_db)):
#     try:
#         recipes = db.query(Categories).filter(Categories.category_name == category).all()
#         if not recipes:
#             raise HTTPException(status_code=404, detail="No recipes found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
#     return JSONResponse(status_code=200, content={"recipes": recipes})