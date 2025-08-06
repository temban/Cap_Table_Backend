from fastapi import APIRouter
from app.controllers import (
    auth_controller,
    shareholder_controller,
    issuance_controller
)

api_router = APIRouter()

api_router.include_router(auth_controller.router, tags=["Authentication"])
api_router.include_router(shareholder_controller.router, prefix="/shareholders", tags=["Shareholders"])
api_router.include_router(issuance_controller.router, prefix="/issuances")
