# FastAPI Scaffold / FastAPI 脚手架

[English](#english) | [中文](#中文)

---

## English

### 🚀 FastAPI Modern Scaffold

A modern, production-ready FastAPI scaffold with async database operations, automatic migrations, and clean architecture.

#### ✨ Features

- **Async Database**: SQLAlchemy + aiosqlite/asyncpg
- **Auto Migrations**: Alembic with automatic model detection
- **Clean Architecture**: Modular structure with repositories, models, schemas
- **API Versioning**: v1 API structure ready for scaling  
- **Environment Management**: Pydantic Settings with .env support
- **Ready to Deploy**: Uvicorn + production configurations

#### 📁 Project Structure

```
fastapi-fast/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Core configs  
│   ├── db/              # Database setup
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── schemas/         # Pydantic schemas
│   └── main.py          # FastAPI app
├── migrations/          # Alembic migrations
├── scripts/             # Utility scripts
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

#### 🏃‍♂️ Quick Start

1. **Clone & Setup**
   ```bash
   git clone <your-repo>
   cd fastapi-fast
   ./scripts/setup.sh
   ```

2. **Run Development Server**
   ```bash
   ./scripts/run.sh
   ```

3. **Access API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

#### 🔄 Database Migrations

Add new models and sync to database:

```bash
# 1. Create model in app/models/your_model.py
# 2. Add import in migrations/env.py
# 3. Generate & apply migration
./scripts/migrate.sh "create your_model table"
```

#### 📝 Adding New Models

1. **Create Model**
   ```python
   # app/models/product.py
   from sqlalchemy import Integer, String
   from sqlalchemy.orm import Mapped, mapped_column
   from app.db.base import Base

   class Product(Base):
       __tablename__ = "products"
       
       id: Mapped[int] = mapped_column(Integer, primary_key=True)
       name: Mapped[str] = mapped_column(String(100))
       price: Mapped[float] = mapped_column(Float)
   ```

2. **Register in Migrations**
   ```python
   # migrations/env.py
   from app.models.product import Product  # noqa
   ```

3. **Generate Migration**
   ```bash
   ./scripts/migrate.sh "create products table"
   ```

#### 🛠 Available Scripts

- `./scripts/setup.sh` - Project setup
- `./scripts/run.sh` - Start development server  
- `./scripts/migrate.sh` - Database migrations
- `./scripts/reset-db.sh` - Reset database

#### 🌍 Environment Variables

```env
PROJECT_NAME=FastAPI App
VERSION=0.1.0
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

#### 🔧 Production Deployment

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 中文

### 🚀 FastAPI 现代化脚手架

一个现代化、生产就绪的 FastAPI 脚手架，支持异步数据库操作、自动迁移和清晰架构。

#### ✨ 特性

- **异步数据库**: SQLAlchemy + aiosqlite/asyncpg
- **自动迁移**: Alembic 自动检测模型变化
- **清晰架构**: 模块化结构，包含仓储、模型、模式层
- **API 版本化**: v1 API 结构，便于扩展
- **环境管理**: Pydantic Settings + .env 支持
- **部署就绪**: Uvicorn + 生产配置

#### 📁 项目结构

```
fastapi-fast/
├── app/
│   ├── api/v1/          # API 路由
│   ├── core/            # 核心配置
│   ├── db/              # 数据库配置
│   ├── models/          # SQLAlchemy 模型
│   ├── repositories/    # 数据访问层
│   ├── schemas/         # Pydantic 模式
│   └── main.py          # FastAPI 应用
├── migrations/          # Alembic 迁移文件
├── scripts/             # 工具脚本
├── requirements.txt     # 依赖列表
└── .env                 # 环境变量
```

#### 🏃‍♂️ 快速开始

1. **克隆并设置**
   ```bash
   git clone <your-repo>
   cd fastapi-fast
   ./scripts/setup.sh
   ```

2. **运行开发服务器**
   ```bash
   ./scripts/run.sh
   ```

3. **访问 API**
   - API: http://localhost:8000
   - 文档: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

#### 🔄 数据库迁移

添加新模型并同步到数据库：

```bash
# 1. 在 app/models/your_model.py 中创建模型
# 2. 在 migrations/env.py 中添加导入
# 3. 生成并执行迁移
./scripts/migrate.sh "create your_model table"
```

#### 📝 添加新模型

1. **创建模型**
   ```python
   # app/models/product.py
   from sqlalchemy import Integer, String, Float
   from sqlalchemy.orm import Mapped, mapped_column
   from app.db.base import Base

   class Product(Base):
       __tablename__ = "products"
       
       id: Mapped[int] = mapped_column(Integer, primary_key=True)
       name: Mapped[str] = mapped_column(String(100))
       price: Mapped[float] = mapped_column(Float)
   ```

2. **在迁移中注册**
   ```python
   # migrations/env.py
   from app.models.product import Product  # noqa
   ```

3. **生成迁移**
   ```bash
   ./scripts/migrate.sh "create products table"
   ```

#### 🛠 可用脚本

- `./scripts/setup.sh` - 项目设置
- `./scripts/run.sh` - 启动开发服务器
- `./scripts/migrate.sh` - 数据库迁移
- `./scripts/reset-db.sh` - 重置数据库

#### 🌍 环境变量

```env
PROJECT_NAME=FastAPI App
VERSION=0.1.0
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

#### 🔧 生产部署

```bash
# 安装生产依赖
pip install gunicorn

# 使用 Gunicorn 运行
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### 💡 标准化工作流程

每次添加新表时的标准流程：

1. **模型定义** → 2. **更新env.py** → 3. **生成迁移** → 4. **执行迁移** → 5. **验证结果**

#### 📋 迁移检查清单

- [ ] 在 `app/models/` 创建模型文件
- [ ] 在 `migrations/env.py` 添加模型导入  
- [ ] 运行 `./scripts/migrate.sh "描述"`
- [ ] 验证数据库表结构
- [ ] 测试 API 功能

---

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.