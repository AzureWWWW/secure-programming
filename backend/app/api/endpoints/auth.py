from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
import schemas.user
from schemas.token import Token
from core.security import hash_password, create_access_token
from core.config import settings
from core.utils import authenticate_user, get_current_active_user
from database import get_db
from datetime import timedelta

router = APIRouter()

@router.post("/register/")
def register(userData: schemas.user.UserCreate, db: Session = Depends(get_db)):
    # check if username, email already exists
    existing_user = db.query(User).filter(User.username == userData.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    existed_email = db.query(User).filter(User.email == userData.email).first()
    if existed_email:
        raise HTTPException(status_code=400, detail="This email has already been used")
    
    hashed_password = hash_password(userData.password)
    
    # create new user object
    db_user = User(
        first_name=userData.first_name,
        last_name=userData.last_name,
        username=userData.username, 
        email=userData.email, 
        hashed_password=hashed_password,
        phone_number=userData.phone_number, 
        role = "user"
        )
    # add new user to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

# User login and return token
@router.post("/token/")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
    ) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=schemas.user.User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user