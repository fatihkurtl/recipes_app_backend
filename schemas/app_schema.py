from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class RecipesBase(BaseModel):
    title: Optional[str]
    title_en: Optional[str]
    description: Optional[str]
    description_en: Optional[str]
    thumbnail_file: Optional[bytes]
    save_count: Optional[int] = 0
    popular: Optional[bool] = False
    active: Optional[bool] = True
    
    class Config:
        orm_mode = True
        from_orm = True
        validate_assignment = True
        arbitrary_types_allowed = True
        populate_by_name = True
        from_attributes = True

class RecipesCreate(RecipesBase):
    category_name: str
    category_name_en: str

class RecipesUpdate(RecipesBase):
    category_name: str
    category_name_en: str

class RecipesInDBBase(RecipesBase):
    id: int
    category_name: str
    category_name_en: str
    create_at: Optional[datetime]
    update_at: Optional[datetime]

    class Config:
        orm_mode = True

class Recipes(RecipesInDBBase):
    pass


############################################

class CategoriesBase(BaseModel):
    id: int
    category_name: str
    category_name_en: str
    description: Optional[str] = None
    description_en: Optional[str] = None
    create_at: datetime
    update_at: datetime
    
    class Config:
        orm_mode = True
        from_orm = True
        validate_assignment = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        from_attributes = True

class CategoriesCreate(BaseModel):
    category_name: str
    category_name_en: str
    description: Optional[str] = None
    description_en: Optional[str] = None

class CategoriesUpdate(BaseModel):
    category_name: Optional[str] = None
    category_name_en: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None

class CategoriesInDBBase(BaseModel):
    categories: List[CategoriesBase]

class CategoriesInResponse(BaseModel):
    id: int
    category_name: str
    category_name_en: str
    description: Optional[str] = None
    description_en: Optional[str] = None
    create_at: Optional[datetime]
    update_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_orm = True