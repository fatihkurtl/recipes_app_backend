from typing import List, Optional
from unicodedata import category
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import all_
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import AppImages, Recipes, Categories
from schemas.app_schema import CategoriesBase, CategoriesInDBBase, RecipesBase, RecipesInDBBase
from .app_helpers import all_categories, get_all_recipes, get_all_recipes_by_category


router = APIRouter(
    prefix="/app/api",
    tags=["app"],
    responses={404: {"description": "Not found"}},
)


@router.get("/recipes/categories", response_model=CategoriesInDBBase)
async def categories(db: Session = Depends(get_db)):
    categories = all_categories(db)
    return {"categories": categories}


@router.get("/recipes", response_model=List[RecipesBase])
async def get_recipes(
    skip: int = 0, 
    limit: int = 10, 
    title: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_all_recipes(db, skip, limit, title, description, category)


@router.get("/recipes/{recipe_category}", response_model=List[RecipesBase])
async def get_recipes_by_category(recipe_category: str, db: Session = Depends(get_db)):
    return get_all_recipes_by_category(db, recipe_category)


