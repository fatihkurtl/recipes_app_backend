from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class RecipesBase(BaseModel):
    title: Optional[str]
    title_en: Optional[str]
    description: Optional[str]
    description_en: Optional[str]
    thumbnail: Optional[str]
    save_count: Optional[int] = 0
    popular: Optional[bool] = False
    active: Optional[bool] = True
    category_id: Optional[int]

class RecipesCreate(RecipesBase):
    pass

class RecipesUpdate(RecipesBase):
    pass

class RecipesInDBBase(RecipesBase):
    id: int
    create_at: Optional[datetime]
    update_at: Optional[datetime]

    class Config:
        orm_mode = True

class Recipes(RecipesInDBBase):
    pass


############################################

class CategoriesBase(BaseModel):
    name: str
    name_en: str
    description: Optional[str] = None
    description_en: Optional[str] = None

class CategoriesCreate(CategoriesBase):
    pass

class CategoriesUpdate(CategoriesBase):
    pass

class CategoriesInDBBase(CategoriesBase):
    id: int
    recipes: List[Recipes]

    class Config:
        orm_mode = True

class Categories(CategoriesInDBBase):
    create_at: Optional[datetime]
    update_at: Optional[datetime]

    class Config:
        orm_mode = True
