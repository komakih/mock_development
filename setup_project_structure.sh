#!/bin/bash

# ディレクトリ作成
mkdir -p api/{chat,users,history,documents,indexing,logs,help,utils} db scripts documents manual_db logs help tests

# __init__.py をすべてのサブフォルダに作成
touch api/{chat,users,history,documents,indexing,logs,help,utils}/__init__.py
touch api/__init__.py db/__init__.py tests/__init__.py

# apiフォルダ内の各ファイルを作成
touch api/chat/chat.py api/users/users.py api/history/history.py api/documents/documents.py api/indexing/indexing.py api/logs/logs.py api/help/help.py api/utils/utils.py

# dbフォルダ内のファイルを作成
touch db/database.py db/models.py

# scriptsフォルダ内のファイルを作成
touch scripts/import_to_chromadb.py scripts/query_chromadb.py scripts/indexing.py

# testsフォルダ内のテストファイル作成
touch tests/test_api.py tests/test_integration.py

# ルートディレクトリに必要なファイルを作成
touch main.py .env pytest.ini requirements.txt

echo "✅ プロジェクト構造が正常に作成されました。"

