from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.models.user_model import User, UserRole
from app.models.issuance_model import ShareIssuance
from app.db.session import SessionLocal
from app.core.security import get_password_hash
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    """Database session fixture"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_and_teardown(db):
    """Clean database and create test users before each test"""
    try:
        # Delete in correct order to respect foreign key constraints
        db.query(ShareIssuance).delete()
        db.query(User).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    
    # Create admin user
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True
    )
    
    # Create shareholder user
    shareholder = User(
        email="shareholder@example.com",
        hashed_password=get_password_hash("shareholderpassword"),
        full_name="Shareholder User",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    
    db.add_all([admin, shareholder])
    db.commit()
    yield

def get_admin_auth_headers():
    """Helper to get admin auth headers"""
    login_response = client.post(
        "/api/v1/token",
        json={"email": "admin@example.com", "password": "adminpassword"}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    token = login_response.json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_shareholder_auth_headers():
    """Helper to get shareholder auth headers"""
    login_response = client.post(
        "/api/v1/token",
        json={"email": "shareholder@example.com", "password": "shareholderpassword"}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    token = login_response.json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_get_issuances_filtering(db):
    """Test that shareholders only see their own issuances while admins see all"""
    # Get test users
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    shareholder = db.query(User).filter(User.email == "shareholder@example.com").first()
    
    # Create test issuances
    issuances = [
        {"shareholder_id": shareholder.id, "number_of_shares": 100},
        {"shareholder_id": shareholder.id, "number_of_shares": 50},
        {"shareholder_id": admin.id, "number_of_shares": 200}
    ]
    
    # Admin creates all issuances
    admin_headers = get_admin_auth_headers()
    for issuance in issuances:
        client.post("/api/v1/issuances", json=issuance, headers=admin_headers)
    
    # Test as shareholder
    shareholder_headers = get_shareholder_auth_headers()
    response = client.get("/api/v1/issuances", headers=shareholder_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Should only see their 2 issuances
    assert all(issuance["shareholder_id"] == str(shareholder.id) for issuance in data)
    
    # Test as admin
    response = client.get("/api/v1/issuances", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3  # Admin sees all

def test_create_issuance(db):
    """Test creating share issuances with validation"""
    admin_headers = get_admin_auth_headers()
    shareholder = db.query(User).filter(User.email == "shareholder@example.com").first()

    # Valid issuance
    issuance_data = {
        "shareholder_id": str(shareholder.id),
        "number_of_shares": 75,
        "price_per_share": 10.50
    }

    response = client.post(
        "/api/v1/issuances",
        json=issuance_data,
        headers=admin_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["number_of_shares"] == 75
    assert data["shareholder_id"] == str(shareholder.id)

    # Test invalid cases
    invalid_cases = [
        ({"number_of_shares": -10}, "negative shares"),
        ({"price_per_share": -5.0}, "negative price"),
        ({"shareholder_id": "00000000-0000-0000-0000-000000000000"}, "invalid shareholder")  # Use a valid UUID format but non-existent
    ]

    for data, description in invalid_cases:
        invalid_data = issuance_data.copy()
        invalid_data.update(data)
        response = client.post(
            "/api/v1/issuances",
            json=invalid_data,
            headers=admin_headers
        )
        assert response.status_code == 400, f"Failed for {description}"
        if description == "invalid shareholder":
            assert "Shareholder not found" in response.json()["detail"]

def test_pdf_certificate_generation(db):
    """Test PDF certificate generation and access control"""
    # Create a test issuance
    admin_headers = get_admin_auth_headers()
    shareholder = db.query(User).filter(User.email == "shareholder@example.com").first()
    
    issuance_data = {
        "shareholder_id": str(shareholder.id),
        "number_of_shares": 100
    }
    response = client.post(
        "/api/v1/issuances",
        json=issuance_data,
        headers=admin_headers
    )
    issuance_id = response.json()["id"]
    
    # Test as shareholder (should work)
    shareholder_headers = get_shareholder_auth_headers()
    response = client.get(
        f"/api/v1/issuances/{issuance_id}/certificate",
        headers=shareholder_headers
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert f"certificate_{issuance_id}.pdf" in response.headers["content-disposition"]
    
    # Test as different user (should fail)
    other_user = User(
        email="other@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Other User",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(other_user)
    db.commit()
    
    other_headers = {
        "Authorization": f"Bearer {get_password_hash('password')}",
        "Content-Type": "application/json"
    }
    response = client.get(
        f"/api/v1/issuances/{issuance_id}/certificate",
        headers=other_headers
    )
    assert response.status_code in [401, 403]  # Either unauthorized or forbidden
    
    # Clean up
    db.delete(other_user)
    db.commit()