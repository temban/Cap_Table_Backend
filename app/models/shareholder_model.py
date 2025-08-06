from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ShareholderProfile(Base):
    __tablename__ = "shareholder_profiles"
    
    id = Column(String, ForeignKey('users.id'), primary_key=True)
    address = Column(String)
    phone = Column(String)
    
    user = relationship("User", back_populates="shareholder_profile")