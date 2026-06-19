#!/bin/bash
# 領標雷達 啟動腳本

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "📡 領標雷達啟動中..."

# 1. 安裝依賴（如需要）
if [ ! -d "backend/.venv" ]; then
  echo "⚙️  建立 Python 虛擬環境..."
  /opt/homebrew/bin/python3.13 -m venv backend/.venv
fi

echo "📦 安裝後端依賴..."
source backend/.venv/bin/activate
pip install -q -r backend/requirements.txt

echo "🌐 啟動後端 (port 8003)..."
cd backend
PYTHONPATH="$SCRIPT_DIR" .venv/bin/uvicorn backend.main:app --reload --port 8003 &
BACKEND_PID=$!
cd ..

echo "⚡ 啟動前端 (port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 領標雷達已啟動！"
echo "   前端：http://localhost:5173"
echo "   後端：http://localhost:8003"
echo "   API 文件：http://localhost:8003/docs"
echo ""
echo "按 Ctrl+C 停止服務"

# Wait for either process
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
