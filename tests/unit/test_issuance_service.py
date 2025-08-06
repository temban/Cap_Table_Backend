import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.services.issuance_service import (
    create_issuance,
    get_issuances,
    get_issuance_by_id,
    get_ownership_distribution
)
from app.models.issuance_model import ShareIssuance
from app.models.user_model import User
from app.schemas.issuance_schema import ShareIssuanceCreate
from fastapi import HTTPException
from sqlalchemy.sql.expression import BinaryExpression

def test_create_issuance_success():
    mock_db = Mock(spec=Session)
    mock_issuance = ShareIssuanceCreate(
        shareholder_id="valid-uuid",
        number_of_shares=100,
        price_per_share=10.0
    )

    # Test successful creation
    result = create_issuance(mock_db, mock_issuance)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_get_issuances_filtered():
    mock_db = Mock(spec=Session)
    mock_query = Mock()
    mock_db.query.return_value = mock_query

    # Test with shareholder_id filter
    get_issuances(mock_db, shareholder_id="test-id")
    
    # Check if filter was called with the correct condition
    assert mock_query.filter.called
    # Get the first argument passed to filter
    filter_arg = mock_query.filter.call_args[0][0]
    assert str(filter_arg) == "share_issuances.shareholder_id = :shareholder_id_1"

def test_get_ownership_distribution():
    mock_db = Mock(spec=Session)
    
    # Mock database response - create proper mock objects with total_shares attribute
    class MockResult:
        def __init__(self, shareholder_id, total_shares):
            self.shareholder_id = shareholder_id
            self.total_shares = total_shares
    
    mock_results = [
        MockResult("user1", 100),
        MockResult("user2", 200)
    ]
    
    mock_db.query.return_value.group_by.return_value.all.return_value = mock_results
    
    # Mock user lookup
    mock_user = Mock()
    mock_user.full_name = "Test User"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    result = get_ownership_distribution(mock_db)
    
    assert len(result) == 2
    assert result[0]["percentage"] == pytest.approx(33.33, 0.1)
    assert result[1]["percentage"] == pytest.approx(66.66, 0.1)