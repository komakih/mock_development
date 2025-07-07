from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User
from api.utils import hash_password
from pydantic import BaseModel, ConfigDict

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    prompt: str = "あなたは優秀なアシスタントです。"

class UserResponse(BaseModel):
    id: int
    username: str
    prompt: str

    model_config = ConfigDict(from_attributes=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="ユーザーが既に存在します")
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        prompt=user.prompt
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user
