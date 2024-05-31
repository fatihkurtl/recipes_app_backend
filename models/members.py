from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database.db import Base

from .app import Recipes



class MemberToken(Base):
    __tablename__ = 'token_table'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(length=255), nullable=False, unique=True, index=True)
    member_id = Column(Integer, ForeignKey('members_table.id'))    
    member = relationship('Members', back_populates='token')
    
    def get_member_token(self):
        return self.token


class SavedRecipes(Base):
    __tablename__ = 'saved_recipes_table'
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes_table.id'))
    recipe = relationship(Recipes, back_populates='saved_recipes')
    member_id = Column(Integer, ForeignKey('members_table.id'))
    member = relationship('Members', back_populates='saved_recipes')
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def get_member_id(self):
        return self.member_id
    
    def get_recipe_id(self):
        return self.recipe_id


class Members(Base):
    __tablename__ = 'members_table'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(length=60), nullable=True)
    username = Column(String(length=60), unique=True, index=True, nullable=True)
    email = Column(String(length=60), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=255), nullable=False)
    last_entry_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)    
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    token = relationship('MemberToken', back_populates='members')
    
    def get_token(self):
        return self.token
    
    def get_new_members(self):
        return self.create_at > datetime.now() - timedelta(days=7)
    
    

