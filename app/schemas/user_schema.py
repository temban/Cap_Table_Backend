from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserRole(str, Enum):
    admin = "admin"
    shareholder = "shareholder"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe"
            }
        }
    )

class UserCreate(UserBase):
    password: str
    role: UserRole
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "password": "strongpassword123",
                "role": "shareholder"
            }
        }
    )

class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    is_disabled: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str