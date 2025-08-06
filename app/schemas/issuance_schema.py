from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user_schema import UserResponse
from pydantic.config import ConfigDict

class ShareIssuanceBase(BaseModel):
    number_of_shares: int
    price_per_share: Optional[float] = None
    issue_date: Optional[datetime] = None

class ShareIssuanceCreate(ShareIssuanceBase):
    shareholder_id: str

class ShareIssuanceResponse(ShareIssuanceBase):
    id: str
    shareholder_id: str
    certificate_url: Optional[str] = None
    shareholder: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class OwnershipDistribution(BaseModel):
    shareholder_id: str
    shareholder_name: str
    total_shares: int
    percentage: float