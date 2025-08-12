#!/bin/bash

# Test Runner Script
# 测试运行脚本

set -e

echo "🧪 Running FastAPI tests..."
echo "🧪 运行 FastAPI 测试..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./scripts/setup.sh first"
    echo "❌ 未找到虚拟环境，请先运行 ./scripts/setup.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Install test dependencies if not installed
echo "📦 Installing test dependencies..."
echo "📦 安装测试依赖..."
pip install pytest httpx pytest-asyncio >/dev/null 2>&1 || {
    echo "❌ Failed to install test dependencies"
    echo "❌ 安装测试依赖失败"
    exit 1
}

# Create test database
echo "🗄️ Setting up test database..."
echo "🗄️ 设置测试数据库..."
if [ -f "app.db" ]; then
    cp app.db app_test.db.bak 2>/dev/null || true
fi

# Run tests
echo "🚀 Running tests..."
echo "🚀 运行测试..."

if [ "$1" = "--coverage" ] || [ "$1" = "-c" ]; then
    echo "📊 Running tests with coverage..."
    echo "📊 运行测试并生成覆盖率报告..."
    pip install pytest-cov >/dev/null 2>&1
    pytest tests/ --cov=app --cov-report=html --cov-report=term-missing -v
    echo ""
    echo "📊 Coverage report generated in htmlcov/"
    echo "📊 覆盖率报告生成在 htmlcov/ 目录"
elif [ "$1" = "--verbose" ] || [ "$1" = "-v" ]; then
    pytest tests/ -v
else
    pytest tests/
fi

# Cleanup
if [ -f "app_test.db.bak" ]; then
    mv app_test.db.bak app.db 2>/dev/null || true
fi

echo ""
echo "✅ Tests completed!"
echo "✅ 测试完成！"

# Show test summary
LAST_EXIT_CODE=$?
if [ $LAST_EXIT_CODE -eq 0 ]; then
    echo "🎉 All tests passed!"
    echo "🎉 所有测试通过！"
else
    echo "❌ Some tests failed"
    echo "❌ 部分测试失败"
    exit $LAST_EXIT_CODE
fi