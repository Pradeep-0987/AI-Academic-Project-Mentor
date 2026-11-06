from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import (
    DuplicateEmailError,
    InvalidCredentialsError,
    login,
    register,
)


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user, token = register(db, request.name, str(request.email), request.password)
    except DuplicateEmailError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        user, token = login(db, str(request.email), request.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
