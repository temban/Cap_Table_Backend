from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.dependencies.auth import get_current_user, get_admin_user
from app.models.issuance_model import ShareIssuance
from app.schemas.issuance_schema import (
    ShareIssuanceCreate,
    ShareIssuanceResponse,
    OwnershipDistribution
)
from app.services.issuance_service import (
    create_issuance,
    get_issuances,
    get_issuance_by_id,
    get_ownership_distribution
)
from app.models.user_model import User, UserRole
from app.utils.pdf_utils import generate_share_certificate
from app.utils.email_utils import send_certificate_email
from app.core.config import settings
import logging

router = APIRouter(tags=["Issuances"])
logger = logging.getLogger(__name__)

def validate_issuance_data(issuance_data: ShareIssuanceCreate, db: Session):
    """Advanced validation for share issuance"""
    if issuance_data.number_of_shares <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of shares must be positive"
        )
    if issuance_data.price_per_share is not None and issuance_data.price_per_share < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Price per share cannot be negative"
        )
    # Validate shareholder exists
    shareholder = db.query(User).filter(User.id == issuance_data.shareholder_id).first()
    if not shareholder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shareholder not found"
        )

@router.post(
    "/",
    response_model=ShareIssuanceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_admin_user)]
)
def create_new_issuance(
    issuance: ShareIssuanceCreate,
    db: Session = Depends(get_db)
):
    """Create new share issuance with automatic email notification"""
    # Validate input
    validate_issuance_data(issuance, db)
    
    # Audit log
    logger.info(f"Creating new share issuance for shareholder {issuance.shareholder_id}")
    
    try:
        # Create the issuance record
        db_issuance = create_issuance(db, issuance)
        
        # Get shareholder details
        shareholder = db.query(User).filter(User.id == issuance.shareholder_id).first()
        if not shareholder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shareholder not found"
            )
        
        # Prepare certificate data
        cert_data = {
            "id": db_issuance.id,
            "number_of_shares": db_issuance.number_of_shares,
            "price_per_share": db_issuance.price_per_share,
            "issue_date": db_issuance.issue_date
        }
        
        # Generate PDF certificate
        pdf_buffer = generate_share_certificate(
            cert_data,
            {
                "id": shareholder.id,
                "full_name": shareholder.full_name
            }
        )
        pdf_bytes = pdf_buffer.read()
        
        # Send email with certificate
        email_sent = send_certificate_email(
            to_email=shareholder.email,
            shareholder_name=shareholder.full_name,
            issuance_data=cert_data,
            pdf_attachment=pdf_bytes
        )
        
        if not email_sent:
            logger.error(f"Failed to send certificate email to {shareholder.email}")
        
        # Update certificate URL in database
        db_issuance.certificate_url = f"/api/v1/issuances/{db_issuance.id}/certificate"
        db.commit()
        db.refresh(db_issuance)
        
        return db_issuance
        
    except Exception as e:
        logger.error(f"Error creating issuance: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create share issuance"
        )

@router.get(
    "/",
    response_model=List[ShareIssuanceResponse]
)
def list_issuances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all issuances (admin sees all, shareholders see only their own)"""
    shareholder_id = None if current_user.role == UserRole.ADMIN else current_user.id
    return get_issuances(db, skip, limit, shareholder_id)

@router.get(
    "/distribution",
    response_model=List[OwnershipDistribution],
    dependencies=[Depends(get_admin_user)]
)
def get_distribution(
    db: Session = Depends(get_db)
):
    """Get ownership distribution data for visualization"""
    return get_ownership_distribution(db)

@router.get(
    "/{issuance_id}/certificate",
    response_class=StreamingResponse
)
def generate_certificate(
    issuance_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate and download a share certificate PDF"""
    issuance = get_issuance_by_id(db, issuance_id)
    if not issuance:
        raise HTTPException(status_code=404, detail="Issuance not found")
    
    # Verify ownership (admin can access any)
    if current_user.role != UserRole.ADMIN and issuance.shareholder_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this certificate")
    
    shareholder = db.query(User).filter(User.id == issuance.shareholder_id).first()
    if not shareholder:
        raise HTTPException(status_code=404, detail="Shareholder not found")
    
    # Generate PDF
    cert_data = {
        "id": issuance.id,
        "number_of_shares": issuance.number_of_shares,
        "price_per_share": issuance.price_per_share,
        "issue_date": issuance.issue_date
    }
    shareholder_data = {
        "id": shareholder.id,
        "full_name": shareholder.full_name
    }
    
    pdf_buffer = generate_share_certificate(cert_data, shareholder_data)
    
    # Audit log
    logger.info(f"Certificate downloaded for issuance {issuance_id} by user {current_user.id}")
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=share_certificate_{issuance.id}.pdf"
        }
    )

@router.get("/test-email")
def test_email(issuance_id: str = Query(...), db: Session = Depends(get_db)):
    """Send a test email using an existing issuance ID"""
    try:
        # 1. Get the issuance record
        issuance = db.query(ShareIssuance).filter(ShareIssuance.id == issuance_id).first()
        if not issuance:
            raise HTTPException(status_code=404, detail="Issuance not found")

        # 2. Get the shareholder (user) associated with the issuance
        shareholder = issuance.shareholder
        print("sdfsdfsdfsdfsdfsdf", shareholder.email.strip())
        print(f"Raw email: {repr(shareholder.email)}")
        if not shareholder:
            raise HTTPException(status_code=404, detail="Shareholder not found")

        # 3. Construct issuance data for the certificate
        cert_data = {
            "id": issuance.id,
            "number_of_shares": issuance.number_of_shares,
            "price_per_share": issuance.price_per_share,
            "issue_date": issuance.issue_date
        }

        # 4. Construct shareholder data
        shareholder_data = {
            "id": shareholder.id,
            "full_name": shareholder.full_name
        }

        # 5. Generate the certificate
        pdf_buffer = generate_share_certificate(cert_data, shareholder_data)
        pdf_bytes = pdf_buffer.getvalue()
        
        # 6. Send the email
        email = shareholder.email.strip()
        success = send_certificate_email(
            to_email=f"{email}",
            shareholder_name=shareholder.full_name,
            issuance_data=cert_data,
            pdf_attachment=pdf_bytes
        )

        return {
            "success": success,
            "message": "Check your inbox and spam folder",
            "shareholder_email": shareholder.email
        }

    except Exception as e:
        return {"error": str(e)}
