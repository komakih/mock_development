import chromadb
from chromadb.utils import embedding_functions
import docx
import os
from dotenv import load_dotenv
import shutil

load_dotenv()
openai_api_key = os.getenv("API_KEY")

persist_directory = "./manual_db"
doc_folder = "./documents"

def rebuild_chromadb_index():
    try:
        # 明示的に環境変数を確認
        telemetry_optout = os.getenv("CHROMADB_TELEMETRY_OPTOUT", "false")
        if telemetry_optout.lower() == "true":
            os.environ["CHROMADB_TELEMETRY_OPTOUT"] = "true"
            print("🚩 ChromaDBのテレメトリーを無効化しました。")

        if os.path.exists(persist_directory):
            shutil.rmtree(persist_directory)

        client = chromadb.PersistentClient(path=persist_directory)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-ada-002"
        )

        collection = client.create_collection("manual_documents", embedding_function=openai_ef)

        doc_paths = [os.path.join(doc_folder, f) for f in os.listdir(doc_folder) if f.endswith(".docx")]
        for path in doc_paths:
            doc = docx.Document(path)
            full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            title = os.path.basename(path).replace(".docx", "")
            collection.add(
                documents=[full_text],
                metadatas=[{"title": title, "path": path}],
                ids=[title]
            )

        print(f"✅ 登録済みドキュメント数: {collection.count()}")
        return {"status": "success", "message": "インデックス更新完了"}

    except Exception as e:
        print(f"🔥 インデックス更新エラー: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    rebuild_chromadb_index()
