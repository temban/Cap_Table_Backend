from typing import Optional
from sqlalchemy.orm import Session
from app.models.issuance_model import ShareIssuance
from app.models.user_model import User
from app.schemas.issuance_schema import ShareIssuanceCreate
from fastapi import HTTPException, status

def create_issuance(db: Session, issuance: ShareIssuanceCreate):
    db_issuance = ShareIssuance(**issuance.model_dump())
    db.add(db_issuance)
    db.commit()
    db.refresh(db_issuance)
    return db_issuance

def get_issuances(db: Session, skip: int = 0, limit: int = 100, shareholder_id: Optional[str] = None):
    query = db.query(ShareIssuance)
    if shareholder_id:
        query = query.filter(ShareIssuance.shareholder_id == shareholder_id)
    return query.offset(skip).limit(limit).all()

def get_issuance_by_id(db: Session, issuance_id: str):
    return db.query(ShareIssuance).filter(ShareIssuance.id == issuance_id).first()

def get_ownership_distribution(db: Session):
    from sqlalchemy import func
    result = db.query(
        ShareIssuance.shareholder_id,
        func.sum(ShareIssuance.number_of_shares).label('total_shares')
    ).group_by(ShareIssuance.shareholder_id).all()
    
    total_company_shares = sum([r.total_shares for r in result]) or 1
    
    distribution = []
    for r in result:
        user = db.query(User).filter(User.id == r.shareholder_id).first()
        distribution.append({
            "shareholder_id": r.shareholder_id,
            "shareholder_name": user.full_name if user else "Unknown",
            "total_shares": r.total_shares,
            "percentage": (r.total_shares / total_company_shares) * 100
        })
    
    return distribution