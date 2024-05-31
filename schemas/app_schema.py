from pydantic import BaseModel

class DrawerHeaderLogo(BaseModel):
    logo: str
    
class CarouselImages(BaseModel):
    images: str