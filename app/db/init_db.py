from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import User  # Import from models package
from app.services.auth_service import get_password_hash

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create initial admin user if not exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("adminpassword"),
                full_name="Admin User",
                role="admin"
            )
            db.add(admin_user)
            db.commit()
        
        # Create initial shareholder user if not exists
        shareholder_user = db.query(User).filter(User.email == "shareholder@example.com").first()
        if not shareholder_user:
            shareholder_user = User(
                email="shareholder@example.com",
                hashed_password=get_password_hash("shareholderpassword"),
                full_name="Shareholder User",
                role="shareholder"
            )
            db.add(shareholder_user)
            db.commit()
    
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()