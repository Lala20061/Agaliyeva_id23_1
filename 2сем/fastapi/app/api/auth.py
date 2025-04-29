from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.cruds.user import create_user, get_user_by_email
from app.core.security import create_access_token, verify_password, get_password_hash, verify_token
from app.schemas.user import UserCreate, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from fastapi import Depends
import logging
from app.core.config import settings

security = HTTPBearer()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sign-up/", response_model=Token)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, email=user.email, password=user.password)
    token = create_access_token(data={"sub": new_user.email})
    return {"id": new_user.id, "email": new_user.email, "token": token}

@router.post("/login/", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"id": db_user.id, "email": db_user.email, "token": token}

@router.post("/login-swagger/", include_in_schema=False)
def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserCreate(email=form_data.username, password=form_data.password)
    return login(user, db)


logging.basicConfig(level=logging.DEBUG)
@router.get("/users/me/")
def read_users_me(token: str = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = verify_token(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email}