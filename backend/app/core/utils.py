# Common helper functions

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from core.security import verify_password, oauth2_scheme
from database import get_db
from models.user import User
from core.config import settings
from schemas.token import TokenData

# Get user from database using username as input
def get_user(username: str, db: Session):
    return db.query(User).filter(User.username==username).first()

# authenticate user
def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # verify token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    

    user = db.query(User).filter(User.username==token_data.username).first()

    if user is None:
        raise credentials_exception
    return user

# get current active user/ valid user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_valid:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Admin role check
def get_current_admin(current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Administrator access required")
    return current_user