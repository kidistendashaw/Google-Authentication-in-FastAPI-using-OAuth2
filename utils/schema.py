from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: Optional[str] = None
    google_id: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    google_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    hashed_password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class GoogleAuthRequest(BaseModel):
    token: str

class GoogleUserInfo(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    google_id: str