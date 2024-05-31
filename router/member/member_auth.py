from fastapi import FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from models.members import Members, MemberToken
from schemas.members_schema import LoginData, RegisterData
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
    return db.query(Members).filter(Members.id == admin_id).first()

def authenticate_admin(db: Session, username: str, password: str):
    admin = db.query(Members).filter(Members.username == username).first()
    if not admin:
        return False
    if not verify_password(password, admin.hashed_password):
        return False
    return admin

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def create_member(db: Session, fullname: str, username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    
    new_member = Members(fullname=fullname, username=username, email=email, hashed_password=hashed_password)
    
    if db.query(Members).filter(Members.email == email).first():
        raise HTTPException(status_code=400, detail="Member email already exists")
    
    if db.query(Members).filter(Members.username == username).first():
        raise HTTPException(status_code=400, detail="Member username already exists")
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return HTTPException(status_code=200, detail="Member created successfully")

def authenticate_member(db: Session, email: str, password: str):
    member = db.query(Members).filter(Members.email == email).first()
    if not member:
        return HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(password, member.hashed_password):
        return HTTPException(status_code=400, detail="Password incorrect")
    token_save = MemberToken(token=create_access_token({"sub": member.username}), member_id=member.id)
    if db.query(MemberToken).filter(MemberToken.member_id == member.id).first():
        raise HTTPException(status_code=400, detail="Token already exists")
    db.add(token_save)
    db.commit()
    access_token = create_access_token(data={"sub": member.username})
    return HTTPException(status_code=200, detail={"access_token": access_token, "token_type": "bearer"})