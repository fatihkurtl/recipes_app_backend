from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RegisterData(BaseModel):
    fullname: str
    username: str
    email: str
    password: str
    
class LoginData(BaseModel):
    email: str
    password: str
    
    
class MemberBase(BaseModel):
    fullname: Optional[str]
    username: Optional[str]
    email: str

class MemberCreate(MemberBase):
    hashed_password: str

class Member(MemberBase):
    id: int
    last_entry_time: Optional[datetime]

    class Config:
        orm_mode = True
