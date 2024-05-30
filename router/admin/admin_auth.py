from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from models.admin import Admin
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import jwt
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_admin(db: Session, admin_id: int):
    return db.query(Admin).filter(Admin.id == admin_id).first()


def authenticate_admin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False
    if not verify_password(password, admin.hashed_password):
        return False
    return admin


def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


def create_admin(db: Session, fullname: str, username: str, email: str, password: str):
    # Şifreyi hash'leyin
    hashed_password = get_password_hash(password)
    
    new_admin = Admin(fullname=fullname, username=username, email=email, hashed_password=hashed_password)
    
    if db.query(Admin).filter(Admin.email == email).first():
        raise HTTPException(status_code=400, detail="Admin email already exists")
    
    if db.query(Admin).filter(Admin.username == username).first():
        raise HTTPException(status_code=400, detail="Admin username already exists")
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return HTTPException(status_code=200, detail="Admin created successfully")


def check_admin(email: str, password: str, db: Session):
    # existing_admin = db.query(Admin).filter(Admin.email == email).first()
    # if existing_admin and existing_admin.hashed_password == password:  # Assuming plain text for simplicity
    #     return existing_admin
    print(email, password)
    return None