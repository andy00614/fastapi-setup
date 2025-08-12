#!/bin/bash

# Database Reset Script
# 数据库重置脚本

set -e

echo "⚠️  WARNING: This will completely reset your database!"
echo "⚠️  警告：这将完全重置您的数据库！"
echo ""
echo "🗄️ This will:"
echo "🗄️ 此操作将："
echo "   • Delete the database file (app.db)"
echo "   • 删除数据库文件 (app.db)"
echo "   • Reset all migration history"
echo "   • 重置所有迁移历史"
echo "   • Recreate the database from scratch"
echo "   • 从头重新创建数据库"
echo ""
echo "❓ Are you sure you want to continue? (y/N)"
echo "❓ 您确定要继续吗？(y/N)"

read -r CONFIRM

if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "🚫 Operation cancelled."
    echo "🚫 操作已取消。"
    exit 0
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./scripts/setup.sh first"
    echo "❌ 未找到虚拟环境，请先运行 ./scripts/setup.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "🗑️ Removing database file..."
echo "🗑️ 删除数据库文件..."
rm -f app.db

echo "🔄 Recreating database..."
echo "🔄 重新创建数据库..."
alembic upgrade head

echo ""
echo "📋 Current database tables:"
echo "📋 当前数据库表:"
if [ -f "app.db" ]; then
    sqlite3 app.db ".tables"
else
    echo "   (No database file found)"
    echo "   (未找到数据库文件)"
fi

echo ""
echo "✅ Database reset completed!"
echo "✅ 数据库重置完成！"
echo ""
echo "💡 You can now start fresh with:"
echo "💡 您现在可以开始使用："
echo "   ./scripts/run.sh"