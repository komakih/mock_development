はい、それでは\*\*「チャットAPIの実装」\*\*について、詳細な内容を明確に整理してご説明します。

チャットAPIの目的は、**ユーザーからの質問に対して、OpenAIのGPTモデルを使って回答を生成し、その内容をDBに保存（会話履歴として）すること**です。

---

## 📌【チャットAPIの実装概要】

**チャットAPIで行う作業**：

* FastAPIを使ったAPIエンドポイント作成（`/chat/query`）
* ユーザーからの質問を受け取り、OpenAI GPT APIを呼び出して回答を生成
* ユーザーごとに設定されたプロンプトを使い、チャット内容をカスタマイズ
* 生成した回答をSQLiteの履歴テーブルに保存（自動化）
* pytestで動作確認用の単体テストを作成

---

## 🚩【実装するファイル】

チャットAPIを実装するファイルは以下のとおりです。

* APIルート定義ファイル：**`api/chat/chat.py`**
* SQLiteのモデル定義ファイル：**`db/models.py`**（すでに完了済みの可能性）
* OpenAI APIキー管理：**`.env`ファイル**

---

## 🔧【Step-by-step 詳細な実装手順】

### ✅ **Step 1: 必要なライブラリの再確認**

プロジェクトで利用するライブラリがインストールされているかを再確認します。

```bash
pip install fastapi openai sqlalchemy python-dotenv uvicorn
```

---

### ✅ **Step 2: DBモデルの再確認（会話履歴保存用モデル）**

`db/models.py`に会話履歴用モデルがあるか確認します（すでに存在する場合は確認のみ）。

```python
from sqlalchemy import Column, Integer, String, DateTime, func
from db.database import Base

class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

すでに作成されている場合は、そのままでOKです。

---

### ✅ **Step 3: チャットAPIルートの作成（`api/chat/chat.py`）**

**実装するチャットAPIルートの例**：

```python
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
        # ユーザーのプロンプトを取得
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

        # OpenAI GPTモデルで回答を生成（ユーザーごとのプロンプトを使用）
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": user.prompt},
                {"role": "user", "content": message}
            ]
        )
        response_text = response.choices[0].message.content

        # 会話履歴をDBに保存
        history_entry = ConversationHistory(
            user_id=user_id,
            message=message,
            response=response_text,
            created_at=datetime.now()
        )
        db.add(history_entry)
        db.commit()

        # GPTからの回答を返却
        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {str(e)}")
```

---

### ✅ **Step 4: FastAPIアプリへのチャットルートの登録（`main.py`）**

`main.py`にチャットAPIルートを追加します。

```python
from fastapi import FastAPI
from db.database import engine, Base
from api.chat import chat  # チャットAPIをインポート

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manual Search AI API")

# チャットAPIを登録
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
```

---

### ✅ **Step 5: pytestによる単体テストの作成（`tests/test_chat.py`）**

`tests/test_chat.py`に以下のテストを追加します：

```python
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
```

---

### ✅ **Step 6: FastAPIを起動して動作確認（Swagger UI）**

FastAPIを起動します：

```bash
uvicorn main:app --reload
```

Swagger UIで確認：

```
http://127.0.0.1:8000/docs
```

* `/chat/query` APIを呼び出して、GPTからの回答が正常に取得できることを確認します。

---

## 📌【最終的な確認チェックリスト】

* [ ] DBモデル（会話履歴テーブル）が存在・構築されている
* [ ] チャットAPIが作成・正常動作確認済み
* [ ] pytestテストが通過済み
* [ ] Swagger UIで動作確認済み（手動テスト）

---

これでチャットAPIの実装は完全に完了です。
ご不明点や追加のご要望がありましたら、お気軽にお知らせください。
