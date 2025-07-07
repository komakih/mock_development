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
