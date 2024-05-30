from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class Admin(Base):
    __tablename__ = 'admin_table'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(length=60), nullable=True)
    username = Column(String(length=60), unique=True, index=True, nullable=True)
    email = Column(String(length=60), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=255), nullable=False)
    last_entry_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    token = relationship('Token', back_populates='admin')
    
class Token(Base):
    __tablename__ = 'token_table'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(length=255), nullable=False, unique=True, index=True)
    admin_id = Column(Integer, ForeignKey('admin_table.id'))    
    admin = relationship('Admin', back_populates='token')
    
    

    