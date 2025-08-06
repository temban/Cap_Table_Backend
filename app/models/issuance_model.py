import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ShareIssuance(Base):
    __tablename__ = "share_issuances"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    shareholder_id = Column(String, ForeignKey('users.id'))
    number_of_shares = Column(Integer, nullable=False)
    price_per_share = Column(Float)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    certificate_url = Column(String)
    
    shareholder = relationship("User", back_populates="issuances")