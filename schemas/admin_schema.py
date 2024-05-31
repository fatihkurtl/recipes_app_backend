from pydantic import BaseModel

class RegisterData(BaseModel):
    fullname: str
    username: str
    email: str
    password: str
    

class LoginData(BaseModel):
    email: str
    password: str
    
class AdminContactData(BaseModel):
    email: str
    subject: str
    message: str
class DrawerHeaderLogo(BaseModel):
    logo: str
    
class CarouselImages(BaseModel):
    images: str