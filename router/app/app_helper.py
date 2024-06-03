from http.client import HTTPException
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.app import AppImages, Recipes, Categories



def get_popular_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Categories).all()
        print('categories', categories)
        if not categories:
            raise HTTPException(status_code=404, detail="No categories found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return JSONResponse(status_code=200, content={"categories": categories})