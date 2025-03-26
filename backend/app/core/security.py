from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from core.config import settings
import bcrypt


ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Hash password using bcrypt
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Verify password using bcrypt
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
