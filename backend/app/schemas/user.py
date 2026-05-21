from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    allowed_tabs: Optional[str] = ""

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None

class UserUpdate(UserBase):
    password: Optional[str] = None
    role_id: Optional[int] = None

class User(UserBase):
    id: int
    role_id: Optional[int] = None
    role: Optional[Role] = None
    created_at: datetime

    class Config:
        from_attributes = True
