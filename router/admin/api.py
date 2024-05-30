from math import e
from typing import Union
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from .admin_auth import check_admin, create_admin
from schemas.admin_schema import LoginData, RegisterData

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},    
)

@router.post("/api/register")
async def register_admin(register_data: RegisterData, db: Session = Depends(get_db)):
    return create_admin(db, register_data.fullname, register_data.username, register_data.email, register_data.password)
    

@router.post("/api/login")
async def login_admin(login_data: LoginData, db: Session = Depends(get_db)):
    admin = check_admin(login_data.email, login_data.password, db)
    if not admin:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Admin login", "admin": admin}
