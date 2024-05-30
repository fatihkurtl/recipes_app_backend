from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from models.admin import Admin, Token
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


def authenticate_admin(db: Session, email: str, password: str):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        return HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(password, admin.hashed_password):
        return HTTPException(status_code=400, detail="Password incorrect")
    token_save = Token(token=create_access_token({"sub": admin.username}), admin_id=admin.id)
    if db.query(Token).filter(Token.admin_id == admin.id).first():
        db.query(Token).filter(Token.admin_id == admin.id).delete()
        db.commit()
        db.add(token_save)
        db.commit()
    access_token = create_access_token(data={"sub": admin.username})        
    return HTTPException(status_code=200, detail={"access_token": access_token, "token_type": "bearer"})