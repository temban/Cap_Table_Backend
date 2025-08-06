from sqlalchemy.orm import Session
from app.models.user_model import User, UserRole
from app.models.shareholder_model import ShareholderProfile
from app.models.issuance_model import ShareIssuance
from app.schemas.shareholder_schema import (
    ShareholderCreate, 
    ShareholderProfileCreate,
    ShareholderUpdate,
    ShareholderProfileUpdate
)
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def get_shareholders(db: Session, skip: int = 0, limit: int = 100):
    """Get all shareholders with their total shares"""
    shareholders = db.query(User).filter(User.role == UserRole.SHAREHOLDER).offset(skip).limit(limit).all()
    
    result = []
    for shareholder in shareholders:
        total_shares = sum(issuance.number_of_shares for issuance in shareholder.issuances)
        result.append({
            "user": shareholder,
            "total_shares": total_shares
        })
    
    return result

def get_shareholder_by_id(db: Session, shareholder_id: str):
    """Get a shareholder by ID with their shares"""
    shareholder = db.query(User).filter(
        User.id == shareholder_id,
        User.role == UserRole.SHAREHOLDER
    ).first()
    
    if not shareholder:
        return None
    
    total_shares = sum(issuance.number_of_shares for issuance in shareholder.issuances)
    
    return {
        "user": shareholder,
        "total_shares": total_shares
    }

def create_shareholder(db: Session, shareholder_data: ShareholderCreate):
    """Create a new shareholder (user + profile)"""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == shareholder_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # Convert to dict and exclude shareholder_profile for user creation
        user_data = shareholder_data.model_dump(exclude={"shareholder_profile"})
        
        # Create the user first
        user = create_user(db, UserCreate(**user_data))
        
        # Create shareholder profile if data provided
        if shareholder_data.shareholder_profile:
            profile_data = shareholder_data.shareholder_profile.model_dump()
            profile = ShareholderProfile(
                id=user.id,
                **profile_data
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
            user.shareholder_profile = profile
        
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


def update_shareholder(db: Session, shareholder_id: str, update_data: ShareholderUpdate):
    """Update shareholder information"""
    shareholder = db.query(User).filter(
        User.id == shareholder_id,
        User.role == UserRole.SHAREHOLDER
    ).first()
    
    if not shareholder:
        return None
    
    # Update user fields
    if update_data.email:
        shareholder.email = update_data.email
    if update_data.full_name:
        shareholder.full_name = update_data.full_name
    if update_data.is_active is not None:
        shareholder.is_active = update_data.is_active
    if update_data.is_disabled is not None:
        shareholder.is_disabled = update_data.is_disabled
    
    # Update profile if exists and data provided
    if update_data.shareholder_profile and shareholder.shareholder_profile:
        profile_data = update_data.shareholder_profile.model_dump(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(shareholder.shareholder_profile, key, value)
    
    db.commit()
    db.refresh(shareholder)
    return shareholder

def deactivate_shareholder(db: Session, shareholder_id: str):
    """Deactivate a shareholder"""
    shareholder = db.query(User).filter(
        User.id == shareholder_id,
        User.role == UserRole.SHAREHOLDER
    ).first()
    
    if not shareholder:
        return None
    
    shareholder.is_active = False
    db.commit()
    db.refresh(shareholder)
    return shareholder