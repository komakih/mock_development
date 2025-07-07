from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI
import os
from dotenv import load_dotenv
from db.database import SessionLocal
from db.models import ConversationHistory, User
from datetime import datetime

load_dotenv()
openai_api_key = os.getenv("API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/query")
def chat_query(message: str, user_id: int, db: Session = Depends(get_db)):
    try:
        # 🚩ユーザーごとのプロンプトを取得
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

        # ユーザーごとのプロンプトをチャットAPIに渡す
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": user.prompt},
                {"role": "user", "content": message}
            ]
        )
        response_text = response.choices[0].message.content

        # 会話履歴を自動保存
        history_entry = ConversationHistory(
            user_id=user_id,
            message=message,
            response=response_text,
            created_at=datetime.now()
        )
        db.add(history_entry)
        db.commit()

        return {"response": response_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
