#!/bin/bash

# FastAPI Project Setup Script
# 快速设置脚本

set -e

echo "🚀 Setting up FastAPI project..."
echo "🚀 正在设置 FastAPI 项目..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "❌ 未安装 Python 3，请先安装 Python 3.8+"
    exit 1
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔗 Activating virtual environment..."
echo "🔗 激活虚拟环境..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
echo "⬆️ 升级 pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📚 Installing dependencies from requirements.txt..."
    echo "📚 从 requirements.txt 安装依赖..."
    pip install -r requirements.txt
else
    echo "📚 Installing basic dependencies..."
    echo "📚 安装基础依赖..."
    pip install fastapi uvicorn sqlalchemy alembic aiosqlite pydantic-settings python-dotenv
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    echo "⚙️ 创建 .env 文件..."
    cat > .env << EOF
PROJECT_NAME=FastAPI App
VERSION=0.1.0
SECRET_KEY=dev-key-please-change-in-production
DATABASE_URL=sqlite+aiosqlite:///./app.db
EOF
fi

# Initialize database
if [ ! -f "app.db" ]; then
    echo "🗄️ Initializing database..."
    echo "🗄️ 初始化数据库..."
    alembic upgrade head
fi

echo ""
echo "✅ Setup completed successfully!"
echo "✅ 设置完成!"
echo ""
echo "🎯 Next steps:"
echo "🎯 下一步:"
echo "   1. Run: ./scripts/run.sh"
echo "   1. 运行: ./scripts/run.sh"
echo "   2. Visit: http://localhost:8000/docs"
echo "   2. 访问: http://localhost:8000/docs"
echo ""