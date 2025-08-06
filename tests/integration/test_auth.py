from app.models.issuance_model import ShareIssuance
from app.models.shareholder_model import ShareholderProfile
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.services.auth_service import get_password_hash
from app.models.user_model import User, UserRole

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

def get_auth_headers(email: str, password: str):
    """Helper function to get auth headers"""
    login_response = client.post("/api/v1/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_register_user(db):
    # Get admin auth headers
    headers = get_auth_headers("admin@example.com", "adminpassword")
    
    # Register new user
    response = client.post(
        "/api/v1/register",
        json={
            "email": "newuser@example.com",
            "password": "newpass123",
            "full_name": "New User",
            "role": "shareholder"
        },
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "shareholder"

def test_login_success(db):
    # Create test user
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("testpass"),
        full_name="Test User",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    # Test login
    response = client.post("/api/v1/login", json={
        "email": "testuser@example.com",
        "password": "testpass"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "testuser@example.com"

def test_login_failure_wrong_password():
    response = client.post("/api/v1/login", json={
        "email": "testuser@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_refresh_token(db):
    # Create test user and get tokens
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("testpass"),
        full_name="Test User",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    login_response = client.post("/api/v1/login", json={
        "email": "testuser@example.com",
        "password": "testpass"
    })
    refresh_token = login_response.json()["refresh_token"]
    
    # Test refresh
    response = client.post("/api/v1/refresh", json={
        "refresh_token": refresh_token
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "testuser@example.com"

def test_refresh_token_invalid():
    response = client.post("/api/v1/refresh", json={
        "refresh_token": "invalidtoken"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"

def test_get_me(db):
    # Create test user and get token
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("testpass"),
        full_name="Test User",
        role=UserRole.SHAREHOLDER,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    headers = get_auth_headers("testuser@example.com", "testpass")
    
    # Test me endpoint
    response = client.get("/api/v1/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data