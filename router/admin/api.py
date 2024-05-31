from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from .admin_auth import authenticate_admin, create_admin, create_admin_contact
from schemas.admin_schema import LoginData, RegisterData, AdminContactData

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
    return authenticate_admin(db, login_data.email, login_data.password)


@router.post("/api/contact")
async def contact_admin(contact_data: AdminContactData, db: Session = Depends(get_db)):
    return create_admin_contact(db, contact_data.email, contact_data.subject, contact_data.message)

