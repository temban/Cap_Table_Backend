from enum import Enum
import uuid
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    SHAREHOLDER = "shareholder"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_disabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Use string references for relationships
    shareholder_profile = relationship("ShareholderProfile", back_populates="user", uselist=False)
    issuances = relationship("ShareIssuance", back_populates="shareholder")

    def __repr__(self):
        return f"<User {self.email}, Role: {self.role}>"