from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from .member_auth import authenticate_member, create_member
from schemas.members_schema import LoginData, RegisterData


router = APIRouter(
    prefix="/member",
    tags=["member"],
    responses={404: {"description": "Not found"}},    
)

@router.post("/api/register")
async def register_member(register_data: RegisterData, db: Session = Depends(get_db)):
    return create_member(db, register_data.fullname, register_data.username, register_data.email, register_data.password)

@router.post("/api/login")
async def login_member(login_data: LoginData, db: Session = Depends(get_db)):
    return authenticate_member(db, login_data.email, login_data.password)



