from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.schemas.user_schema import UserCreate, UserRole, UserResponse

class ShareholderProfileBase(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "address": "123 Main St, City, Country",
                "phone": "+1234567890"
            }
        }
    )

class ShareholderProfileCreate(ShareholderProfileBase):
    pass

class ShareholderProfileUpdate(ShareholderProfileBase):
    pass

class ShareholderProfileResponse(ShareholderProfileBase):
    id: str
    
    model_config = ConfigDict(from_attributes=True)

class ShareIssuanceResponse(BaseModel):
    id: str
    number_of_shares: int
    price_per_share: Optional[float] = None
    issue_date: datetime
    certificate_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ShareholderWithSharesResponse(UserResponse):
    shareholder_profile: Optional[ShareholderProfileResponse] = None
    total_shares: int = 0
    issuances: List[ShareIssuanceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class ShareholderCreate(UserCreate):
    shareholder_profile: Optional[ShareholderProfileCreate] = None
    role: str = "shareholder"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "shareholder@example.com",
                "full_name": "Jane Smith",
                "password": "strongpassword123",
                "role": "shareholder",
                "shareholder_profile": {
                    "address": "123 Main St, City, Country",
                    "phone": "+1234567890"
                }
            }
        }
    )

class ShareholderUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_disabled: Optional[bool] = None
    shareholder_profile: Optional[ShareholderProfileUpdate] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "updated@example.com",
                "full_name": "Updated Name",
                "is_active": True,
                "is_disabled": False,
                "shareholder_profile": {
                    "address": "456 New St, City, Country",
                    "phone": "+9876543210"
                }
            }
        }
    )