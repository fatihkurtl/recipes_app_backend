from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
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
    
    

class Contact(Base):
    __tablename__ = 'contact_table'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=60), nullable=False)
    subject = Column(String(length=200), nullable=False)
    message = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return self.email
    
    def get_latest_contact(self):
        return self.create_at > datetime.now() - timedelta(days=7)
    
    def get_new_contact(self):
        return self.create_at > datetime.now() - timedelta(days=1)
    
    def get_old_contact(self):
        return self.create_at < datetime.now() - timedelta(days=1)
    
    def get_contact_by_email(self, email: str):
        return self.email == email