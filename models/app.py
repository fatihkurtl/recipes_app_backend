from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database.db import Base
from sqlalchemy.orm import Session
import json

class Categories(Base):
    __tablename__ = 'categories_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=80), nullable=False, unique=True, index=True)
    name_en = Column(String(length=80), nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    recipes = relationship('Recipes', back_populates='category')
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return self.name
    
    def get_latest_category(self):
        return self.create_at > datetime.now() - timedelta(days=7)
    
    @staticmethod
    def get_popular_categories(db: Session, min_save_count: int = 10):
        popular_categories = (
            db.query(Categories, func.sum(Recipes.save_count).label('total_saves'))
            .join(Recipes, Categories.id == Recipes.category_id)
            .group_by(Categories.id)
            .having(func.sum(Recipes.save_count) > min_save_count)
            .order_by(func.sum(Recipes.save_count).desc())
            .all()
        )
        return popular_categories

class Recipes(Base):
    __tablename__ = 'recipes_table'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=80), nullable=True, unique=True, index=True)
    title_en = Column(String(length=80), nullable=True, unique=True, index=True)
    description = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    thumbnail = Column(String(length=255), nullable=True)
    save_count = Column(Integer, default=0, nullable=True)
    popular = Column(Integer, default=False, nullable=True)
    active = Column(Integer, default=True, nullable=True)
    category_id = Column(Integer, ForeignKey('categories_table.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return self.title
    
    def get_latest_recipe(self):
        return self.create_at > datetime.now() - timedelta(days=7)
    
    def get_popular_recipe(self):
        return self.save_count > 10
    

class AppImages(Base):
    __tablename__ = 'app_images_table'
    id = Column(Integer, primary_key=True, index=True)
    drawer_header_logo = Column(String(length=255), nullable=True)
    carousel_images = Column(String, nullable=True)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def add_carousel_image(self, image_url: str):
        if self.carousel_images:
            images = json.loads(self.carousel_images)
        else:
            images = []
        images.append(image_url)
        self.carousel_images = json.dumps(images)

    def get_carousel_images(self):
        if self.carousel_images:
            return json.loads(self.carousel_images)
        return []