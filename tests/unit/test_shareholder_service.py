import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.services.shareholder_service import (
    get_shareholders,
    get_shareholder_by_id,
    create_shareholder,
    update_shareholder,
    deactivate_shareholder
)
from app.models.user_model import User, UserRole
from app.schemas.shareholder_schema import ShareholderCreate, ShareholderProfileCreate
from app.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session

def test_get_shareholders_with_shares():
    mock_db = Mock()
    mock_user = Mock(spec=User)
    mock_user.role = UserRole.SHAREHOLDER
    mock_user.issuances = [Mock(number_of_shares=100), Mock(number_of_shares=50)]
    
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [mock_user]
    
    result = get_shareholders(mock_db)
    assert len(result) == 1
    assert result[0]["total_shares"] == 150

def test_create_shareholder_success():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    data = ShareholderCreate(
        email="test@example.com",
        password="password",
        full_name="Test User",
        role=UserRole.SHAREHOLDER,
        shareholder_profile=ShareholderProfileCreate(address="123 Test St")
    )
    
    with patch("app.services.shareholder_service.create_user") as mock_create_user:
        mock_create_user.return_value = Mock(id="new-user-id")
        result = create_shareholder(mock_db, data)
        
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

def test_deactivate_shareholder():
    mock_db = Mock()
    mock_shareholder = Mock(spec=User)
    mock_shareholder.role = UserRole.SHAREHOLDER
    mock_shareholder.is_active = True
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_shareholder
    
    result = deactivate_shareholder(mock_db, "shareholder-id")
    assert result.is_active is False
    mock_db.commit.assert_called_once()