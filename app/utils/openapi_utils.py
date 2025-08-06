from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from typing import Dict, Any

def custom_openapi(app: FastAPI):
    def inner():
        if app.openapi_schema:
            return app.openapi_schema
        
        # First get the base OpenAPI schema
        openapi_schema = get_openapi(
            title="Cap Table Management API",
            version="1.0.0",
            description="API for managing company capitalization tables",
            routes=app.routes,
        )
        
        # Ensure components exist
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}
        
        # Add security scheme
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter: Bearer <token>"
            }
        }
        
        # Ensure schemas exist under components
        if "schemas" not in openapi_schema["components"]:
            openapi_schema["components"]["schemas"] = {}
        
        # Secure all paths that need authentication
        paths_to_secure = [
            "/api/v1/register",
            "/api/v1/me",
            "/api/v1/refresh",
            "/api/v1/shareholders/",
            "/api/v1/shareholders/{shareholder_id}",
            "/api/v1/issuances/",
            "/api/v1/issuances/{issuance_id}/certificate",
            "/api/v1/issuances/distribution"
        ]
        
        for path in paths_to_secure:
            if path in openapi_schema["paths"]:
                for method in openapi_schema["paths"][path]:
                    if method.lower() in ["get", "post", "put", "delete"]:
                        # Initialize security if not exists
                        if "security" not in openapi_schema["paths"][path][method]:
                            openapi_schema["paths"][path][method]["security"] = []
                        # Add our security requirement
                        openapi_schema["paths"][path][method]["security"].append({"BearerAuth": []})
        
        return openapi_schema
    return inner