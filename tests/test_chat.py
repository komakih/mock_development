import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import Base, engine
from db.models import User
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)

    # テスト用ユーザーを作成
    test_user = User(
        username="testuser",
        hashed_password="hashedpassword",
        prompt="あなたはカスタマーサポートAIです。"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()

def test_chat_query():
    # テスト用チャットAPIの呼び出し
    response = client.post("/chat/query", params={"message": "返品方法を教えてください", "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
