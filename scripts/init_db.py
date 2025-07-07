import sys
import os
# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import engine, Base
from db.models import User, ConversationHistory

def init_db():
    print("🚩 データベースを初期化しています...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ データベースの再構築が完了しました。")

if __name__ == "__main__":
    init_db()
