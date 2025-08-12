#!/bin/bash

# Project Health Check Script
# 项目健康检查脚本

set -e

echo "🔍 FastAPI Project Health Check"
echo "🔍 FastAPI 项目健康检查"
echo "================================"
echo ""

# Check Python version
echo "🐍 Python Version:"
python3 --version
echo ""

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "✅ Virtual environment: Found"
    echo "✅ 虚拟环境: 已找到"
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Check installed packages
    echo ""
    echo "📦 Key Dependencies:"
    echo "📦 主要依赖:"
    pip list | grep -E "(fastapi|uvicorn|sqlalchemy|alembic|pydantic)" || echo "   Some dependencies may be missing"
    
else
    echo "❌ Virtual environment: Not found"
    echo "❌ 虚拟环境: 未找到"
    echo "   Run: ./scripts/setup.sh"
    echo "   运行: ./scripts/setup.sh"
fi

echo ""

# Check .env file
if [ -f ".env" ]; then
    echo "✅ Environment file: Found"
    echo "✅ 环境文件: 已找到"
    echo "   Variables:"
    echo "   变量:"
    grep -E "^[A-Z_]+=" .env | sed 's/=.*/=***/' || true
else
    echo "❌ Environment file: Not found"
    echo "❌ 环境文件: 未找到"
fi

echo ""

# Check database
if [ -f "app.db" ]; then
    echo "✅ Database: Found"
    echo "✅ 数据库: 已找到"
    echo "   Tables:"
    echo "   表:"
    sqlite3 app.db ".tables" 2>/dev/null | sed 's/^/     /' || echo "     Unable to read database"
    
    # Check migration status if virtual env exists
    if [ -d ".venv" ]; then
        source .venv/bin/activate
        echo ""
        echo "🔄 Migration Status:"
        echo "🔄 迁移状态:"
        alembic current 2>/dev/null || echo "     Unable to check migration status"
    fi
else
    echo "❌ Database: Not found"
    echo "❌ 数据库: 未找到"
    echo "   Run: alembic upgrade head"
    echo "   运行: alembic upgrade head"
fi

echo ""

# Check if server is running
if lsof -i :8000 >/dev/null 2>&1; then
    echo "🟢 Server Status: Running on port 8000"
    echo "🟢 服务器状态: 运行在端口 8000"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
else
    echo "⚪ Server Status: Not running"
    echo "⚪ 服务器状态: 未运行"
    echo "   Start with: ./scripts/run.sh"
    echo "   启动命令: ./scripts/run.sh"
fi

echo ""

# Check project structure
echo "📁 Project Structure:"
echo "📁 项目结构:"
for dir in app migrations scripts; do
    if [ -d "$dir" ]; then
        echo "   ✅ $dir/"
    else
        echo "   ❌ $dir/ (missing)"
    fi
done

for file in requirements.txt README.md .gitignore; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
    fi
done

echo ""
echo "🏁 Health check completed!"
echo "🏁 健康检查完成！"