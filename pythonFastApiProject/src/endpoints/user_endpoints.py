from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import src.models
import src.crud.user_crud
from src.schemas.user_schema import User, UserInDB, UserBase
from src.database import SessionLocal, engine
from src.auth.auth import authenticate_user, create_access_token, get_current_active_user


src.models.Base.metadata.create_all(bind=engine)


user_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/register/", response_model=User)
def create_user(user: UserInDB, db: Session = Depends(get_db)):
    db_user = src.crud.user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return src.crud.user_crud.create_user(db=db, user=user)


@user_router.get("/users/me/", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user
