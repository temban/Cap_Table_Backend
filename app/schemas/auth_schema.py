from pydantic import BaseModel, Field, ConfigDict

class LoginRequest(BaseModel):
    email: str
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "password": "adminpassword"
            }
        }
    )

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "new.user@example.com",
                "password": "strongpassword123",
                "full_name": "John Doe",
                "role": "shareholder"
            }
        }
    )