from pydantic import BaseModel, EmailStr, Field, field_validator, validator
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: str

    @validator('password')
    def password_max_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long, max 72 bytes')
        return v

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    role: str    

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class TokenIn(BaseModel):
    access_token: str    