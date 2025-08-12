#!/bin/bash

# FastAPI Development Server Runner
# FastAPI 开发服务器启动脚本

set -e

echo "🚀 Starting FastAPI development server..."
echo "🚀 启动 FastAPI 开发服务器..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./scripts/setup.sh first"
    echo "❌ 未找到虚拟环境，请先运行 ./scripts/setup.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if port 8000 is in use
if lsof -i :8000 >/dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use. Trying to kill existing processes..."
    echo "⚠️  端口 8000 已被占用，尝试停止现有进程..."
    pkill -f "uvicorn.*8000" || true
    sleep 2
fi

# Start the server
echo "📡 Server will be available at:"
echo "📡 服务器地址:"
echo "   • API: http://localhost:8000"
echo "   • Docs: http://localhost:8000/docs"
echo "   • ReDoc: http://localhost:8000/redoc"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo "💡 按 Ctrl+C 停止服务器"
echo ""

# Start uvicorn with reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000