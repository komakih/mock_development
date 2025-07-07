from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import ConversationHistory
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter()

class ConversationCreate(BaseModel):
    user_id: int
    message: str
    response: str

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    response: str
    created_at: datetime
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ConversationResponse)
def save_conversation(conv: ConversationCreate, db: Session = Depends(get_db)):
    new_conv = ConversationHistory(
        user_id=conv.user_id,
        message=conv.message,
        response=conv.response
    )
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return new_conv

@router.get("/{user_id}", response_model=List[ConversationResponse])
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(ConversationHistory).filter(ConversationHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="履歴が見つかりません")
    return history
