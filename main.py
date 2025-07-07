from fastapi import FastAPI
from db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SQLite DBが正常に構築されました"}
