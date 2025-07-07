from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    prompt = Column(String, default="あなたは優秀なアシスタントです。")

    # 会話履歴へのリレーション設定
    conversations = relationship("ConversationHistory", back_populates="user")

class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # ユーザーへのリレーション設定
    user = relationship("User", back_populates="conversations")
