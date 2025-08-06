from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.dependencies.auth import get_admin_user as get_current_admin_user
from app.schemas.shareholder_schema import (
    ShareholderProfileResponse,
    ShareholderWithSharesResponse,
    ShareholderCreate,
    ShareholderUpdate
)
from app.services.shareholder_service import (
    get_shareholders,
    get_shareholder_by_id,
    create_shareholder,
    update_shareholder,
    deactivate_shareholder
)
from app.models.user_model import User

router = APIRouter(
    tags=["Shareholders"],
    dependencies=[Depends(get_current_admin_user)]  # All endpoints in this router require admin
)

@router.get(
    "/",
    response_model=List[ShareholderWithSharesResponse],
    summary="List all shareholders",
    description="Retrieve a list of all shareholders with their total shares (Admin only)"
)
def list_shareholders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    shareholders_data = get_shareholders(db, skip=skip, limit=limit)
    return [
        build_shareholder_response(
            shareholder_data["user"],
            shareholder_data["total_shares"]
        )
        for shareholder_data in shareholders_data
    ]

@router.post(
    "/",
    response_model=ShareholderWithSharesResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new shareholder",
    description="Create a new shareholder account (Admin only)"
)
def create_new_shareholder(
    shareholder: ShareholderCreate,
    db: Session = Depends(get_db)
):
    if shareholder.role != "shareholder":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only create shareholders through this endpoint"
        )
    
    db_user = create_shareholder(db, shareholder)
    return build_shareholder_response(db_user, 0)

@router.get(
    "/{shareholder_id}",
    response_model=ShareholderWithSharesResponse,
    summary="Get shareholder by ID",
    description="Retrieve detailed information about a specific shareholder (Admin only)"
)
def get_shareholder(
    shareholder_id: str,
    db: Session = Depends(get_db)
):
    shareholder_data = get_shareholder_by_id(db, shareholder_id)
    if not shareholder_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shareholder not found"
        )
    return build_shareholder_response(
        shareholder_data["user"],
        shareholder_data["total_shares"]
    )

@router.put(
    "/{shareholder_id}",
    response_model=ShareholderWithSharesResponse,
    summary="Update shareholder",
    description="Update shareholder information (Admin only)"
)
def update_shareholder_info(
    shareholder_id: str,
    shareholder_data: ShareholderUpdate,
    db: Session = Depends(get_db)
):
    db_user = update_shareholder(db, shareholder_id, shareholder_data)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shareholder not found"
        )
    total_shares = sum(issuance.number_of_shares for issuance in db_user.issuances)
    return build_shareholder_response(db_user, total_shares)

@router.delete(
    "/{shareholder_id}",
    response_model=ShareholderWithSharesResponse,
    summary="Deactivate shareholder",
    description="Deactivate a shareholder account (Admin only)"
)
def deactivate_shareholder_account(
    shareholder_id: str,
    db: Session = Depends(get_db)
):
    db_user = deactivate_shareholder(db, shareholder_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shareholder not found"
        )
    total_shares = sum(issuance.number_of_shares for issuance in db_user.issuances)
    return build_shareholder_response(db_user, total_shares)

# Helper function to build consistent responses
def build_shareholder_response(user: User, total_shares: int):
    profile = user.shareholder_profile
    profile_response = None
    if profile:
        profile_response = ShareholderProfileResponse(
            id=profile.id,
            address=profile.address,
            phone=profile.phone
        )
    
    return ShareholderWithSharesResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        is_active=user.is_active,
        is_disabled=user.is_disabled,
        created_at=user.created_at,
        updated_at=user.updated_at,
        total_shares=total_shares,
        shareholder_profile=profile_response,
        issuances=user.issuances
    )