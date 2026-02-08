from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from psycopg2 import IntegrityError

from app.config import settings
from app.auth.schemas import (
    RefreshRequest,
    TokenResponse,
    UserInfo,
    UserLogin,
    UserRegister,
)
from app.auth import db as auth_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "type": "access"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "type": "refresh"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInfo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = auth_db.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return UserInfo(**user)


@router.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister):
    hashed = hash_password(data.password)
    try:
        user = auth_db.create_user(data.username, data.email, hashed)
    except (IntegrityError, Exception) as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )
        raise
    if user is None:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return UserInfo(**user)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin):
    user = auth_db.get_user_by_username(data.username)
    if user is None or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return TokenResponse(
        access_token=create_access_token(user["user_id"]),
        refresh_token=create_refresh_token(user["user_id"]),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest):
    try:
        payload = jwt.decode(data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if user_id is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = auth_db.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return TokenResponse(
        access_token=create_access_token(int(user_id)),
        refresh_token=create_refresh_token(int(user_id)),
    )


@router.get("/me", response_model=UserInfo)
def me(current_user: UserInfo = Depends(get_current_user)):
    return current_user
