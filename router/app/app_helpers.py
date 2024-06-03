from http.client import HTTPException
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import Categories, Recipes
from schemas.app_schema import CategoriesBase, RecipesBase


def all_categories(db: Session):
    try:
        categories = db.query(Categories).all()
        if not categories:
            raise HTTPException(status_code=404, detail="No categories found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return [CategoriesBase.from_orm(category) for category in categories]


def get_all_recipes(db: Session, skip, limit, title=None, description=None, category=None):
    try:
        query = db.query(Recipes)
        
        if title:
            query = query.filter(Recipes.title.contains(title))
        if description:
            query = query.filter(Recipes.description.contains(description))
        if category:
            query = query.join(Categories).filter(Categories.category_name_en == category)
        
        recipes = query.offset(skip).limit(limit).all()
        
        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return [RecipesBase.from_orm(recipe) for recipe in recipes]


def get_all_recipes_by_category(db: Session, category: str):
    try:
        category = db.query(Categories).filter(Categories.category_name_en == category).first()
        
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        
        recipes = db.query(Recipes).filter(Recipes.category_id == category.id).all()
        
        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes found for this category")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return [RecipesBase.from_orm(recipe) for recipe in recipes]



# def all_recipes(db: Session):
#     try:
#         recipes = db.query(Recipes).all()
#         if not recipes:
#             raise HTTPException(status_code=404, detail="No recipes found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
#     return [RecipesBase.from_orm(recipe) for recipe in recipes] 