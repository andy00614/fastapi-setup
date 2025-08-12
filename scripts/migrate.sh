#!/bin/bash

# Database Migration Script
# 数据库迁移脚本

set -e

# Check if message is provided
if [ -z "$1" ]; then
    echo "❌ Usage: ./scripts/migrate.sh \"migration message\""
    echo "❌ 用法: ./scripts/migrate.sh \"迁移说明\""
    echo ""
    echo "📝 Example:"
    echo "📝 示例:"
    echo "   ./scripts/migrate.sh \"create users table\""
    echo "   ./scripts/migrate.sh \"add email field to users\""
    exit 1
fi

MESSAGE="$1"

echo "🔄 Running database migration..."
echo "🔄 执行数据库迁移..."
echo "📝 Message: $MESSAGE"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./scripts/setup.sh first"
    echo "❌ 未找到虚拟环境，请先运行 ./scripts/setup.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Show current migration status
echo "📊 Current migration status:"
echo "📊 当前迁移状态:"
alembic current
echo ""

# Generate migration
echo "🔧 Generating migration..."
echo "🔧 生成迁移文件..."
alembic revision --autogenerate -m "$MESSAGE"

# Show what will be migrated
echo ""
echo "📋 Generated migration files:"
echo "📋 生成的迁移文件:"
ls -la migrations/versions/ | tail -n 1

echo ""
echo "❓ Do you want to apply this migration? (y/N)"
echo "❓ 是否要应用此迁移？(y/N)"
read -r CONFIRM

if [[ $CONFIRM =~ ^[Yy]$ ]]; then
    echo "⚡ Applying migration..."
    echo "⚡ 应用迁移..."
    alembic upgrade head
    
    echo ""
    echo "📊 New migration status:"
    echo "📊 新的迁移状态:"
    alembic current
    
    echo ""
    echo "✅ Migration completed successfully!"
    echo "✅ 迁移完成!"
    
    # Show current database tables
    if [ -f "app.db" ]; then
        echo ""
        echo "📋 Current database tables:"
        echo "📋 当前数据库表:"
        sqlite3 app.db ".tables"
    fi
else
    echo "🚫 Migration not applied. You can apply it later with:"
    echo "🚫 迁移未应用，您可以稍后使用以下命令应用:"
    echo "   alembic upgrade head"
fi