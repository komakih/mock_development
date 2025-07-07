import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

# .envから環境変数を読み込み
load_dotenv()
openai_api_key = os.getenv("API_KEY")

# データのディレクトリ設定
persist_directory = os.path.abspath("./manual_db")

# クライアント初期化
client = chromadb.PersistentClient(path=persist_directory)

# OpenAIの埋め込み関数を設定
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-ada-002"
)

def check_chromadb_contents():
    try:
        # 存在するコレクション名を表示
        collections = client.list_collections()
        collection_names = [col.name for col in collections]
        print(f"🚩 存在するコレクション一覧: {collection_names}")

        # 指定のコレクションが存在するか確認
        if "manual_documents" in collection_names:
            collection = client.get_collection(
                "manual_documents",
                embedding_function=openai_ef
            )
            doc_count = collection.count()
            print(f"✅ コレクション 'manual_documents' のドキュメント数: {doc_count}")

            # ドキュメント情報の取得と表示
            results = collection.get()
            for doc_id, metadata in zip(results['ids'], results['metadatas']):
                print(f"📄 ドキュメントID: {doc_id}, タイトル: {metadata.get('title', '未設定')}, パス: {metadata.get('path', '未設定')}")

        else:
            print("❌ コレクション 'manual_documents' が存在しません。")

    except Exception as e:
        print(f"🔥 ChromaDBデータ取得エラー: {e}")

if __name__ == "__main__":
    check_chromadb_contents()
