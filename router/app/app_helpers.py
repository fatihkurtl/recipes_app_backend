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



# def all_recipes(db: Session):
#     try:
#         recipes = db.query(Recipes).all()
#         if not recipes:
#             raise HTTPException(status_code=404, detail="No recipes found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
#     return [RecipesBase.from_orm(recipe) for recipe in recipes] 