from unittest.mock import Mock, patch
import pytest
from datetime import timedelta
from app.services.auth_service import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    authenticate_user
)
from app.core.config import SECRET_KEY, ALGORITHM
from jose import jwt
from sqlalchemy.orm import Session

def test_password_hashing():
    plain_password = "test123"
    hashed = get_password_hash(plain_password)
    assert verify_password(plain_password, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_token_creation_and_verification():
    test_data = {"sub": "test@example.com"}
    
    # Test access token
    access_token = create_access_token(test_data)
    decoded = verify_token(access_token)
    assert decoded["sub"] == "test@example.com"
    assert decoded["type"] == "access"
    
    # Test refresh token
    refresh_token = create_refresh_token(test_data)
    decoded = verify_token(refresh_token)
    assert decoded["type"] == "refresh"

def test_authenticate_user():
    mock_db = Mock()
    mock_user = Mock()
    mock_user.hashed_password = get_password_hash("correct")
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Test correct credentials
    assert authenticate_user(mock_db, "test@example.com", "correct") is not False
    
    # Test wrong password
    assert authenticate_user(mock_db, "test@example.com", "wrong") is False
    
    # Test non-existent user
    mock_db.query.return_value.filter.return_value.first.return_value = None
    assert authenticate_user(mock_db, "nonexistent@example.com", "any") is False