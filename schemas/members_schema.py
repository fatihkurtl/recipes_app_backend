from pydantic import BaseModel

class RegisterData(BaseModel):
    fullname: str
    username: str
    email: str
    password: str
    
class LoginData(BaseModel):
    email: str
    password: str
