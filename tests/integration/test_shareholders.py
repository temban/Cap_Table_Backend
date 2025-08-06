from datetime import datetime
from app.models.issuance_model import ShareIssuance
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.user_model import User, UserRole
from app.models.shareholder_model import ShareholderProfile
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError

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
    """Clean database and create test admin before each test"""
    try:
        # Delete in correct order to respect foreign key constraints
        db.query(ShareIssuance).delete()
        db.query(ShareholderProfile).delete()
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
    db.add(admin)
    db.commit()
    yield

def get_admin_auth_headers():
    """Helper to get admin auth headers"""
    login_response = client.post(
        "/api/v1/login",
        json={"email": "admin@example.com", "password": "adminpassword"}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    token = login_response.json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_list_shareholders(db):
    """Test listing all shareholders"""
    # Create test data
    shareholder1 = User(
        email="shareholder1@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Shareholder One",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    shareholder2 = User(
        email="shareholder2@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Shareholder Two",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add_all([shareholder1, shareholder2])
    db.commit()
    
    # Make request
    headers = get_admin_auth_headers()
    response = client.get("/api/v1/shareholders/", headers=headers)
    
    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_create_shareholder(db):
    """Test creating a new shareholder"""
    headers = get_admin_auth_headers()
    unique_email = f"test_{datetime.now().timestamp()}@example.com"
    
    shareholder_data = {
        "email": unique_email,
        "password": "newpassword123",
        "full_name": "New Shareholder",
        "role": "shareholder",
        "shareholder_profile": {
            "address": "123 Main St",
            "phone": "+1234567890"
        }
    }
    
    response = client.post(
        "/api/v1/shareholders/",
        json=shareholder_data,
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email

def test_get_shareholder_by_id(db):
    """Test getting shareholder by ID"""
    # Create test shareholder
    shareholder = User(
        email="test.shareholder@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test Shareholder",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(shareholder)
    db.commit()
    
    headers = get_admin_auth_headers()
    response = client.get(
        f"/api/v1/shareholders/{shareholder.id}",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(shareholder.id)

def test_update_shareholder(db):
    """Test updating shareholder information"""
    # Create test user first
    shareholder = User(
        email="update.test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Update Test",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(shareholder)
    db.commit()
    db.refresh(shareholder)
    
    # Now create profile with proper ID
    profile = ShareholderProfile(
        id=shareholder.id,  # This is critical
        address="Old Address",
        phone="+0000000000"
    )
    db.add(profile)
    db.commit()
    
    headers = get_admin_auth_headers()
    update_data = {
        "full_name": "Updated Name",
        "shareholder_profile": {
            "address": "New Address"
        }
    }
    
    response = client.put(
        f"/api/v1/shareholders/{shareholder.id}",
        json=update_data,
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_deactivate_shareholder(db):
    """Test deactivating a shareholder"""
    # Create test shareholder
    shareholder = User(
        email="deactivate.test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Deactivate Test",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(shareholder)
    db.commit()

    headers = get_admin_auth_headers()
    response = client.delete(
        f"/api/v1/shareholders/{shareholder.id}",
        headers=headers
    )

    assert response.status_code == 200