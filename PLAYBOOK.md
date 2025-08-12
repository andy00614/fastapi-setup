# FastAPI + Alembic 动态添加表的标准流程

## 📋 完整步骤清单

### 步骤1: 创建新的SQLAlchemy模型
```bash
# 在 app/models/ 目录下创建新的模型文件
touch app/models/user.py
```

### 步骤2: 定义模型结构
在 `app/models/user.py` 中定义模型：
```python
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

### 步骤3: 更新 Alembic 配置
在 `migrations/env.py` 中添加新模型的导入：
```python
# 在现有导入后添加
from app.models.user import User  # noqa
```

### 步骤4: 生成迁移文件
```bash
source .venv/bin/activate && alembic revision --autogenerate -m "create users table"
```

### 步骤5: 执行迁移
```bash
source .venv/bin/activate && alembic upgrade head
```

### 步骤6: 验证表创建
```bash
sqlite3 app.db ".tables"  # 查看所有表
sqlite3 app.db ".schema users"  # 查看users表结构
```

### 步骤7: 创建 Pydantic 模式 (可选)
```bash
touch app/schemas/user.py
```

### 步骤8: 创建 API 端点 (可选)
```bash
touch app/api/v1/users.py
```

### 步骤9: 测试 API (可选)
```bash
curl -s http://localhost:8000/api/v1/users/ | python3 -m json.tool
```

## 🔄 标准化工作流程

每次添加新表时，按此顺序执行：

1. **模型定义** → 2. **更新env.py** → 3. **生成迁移** → 4. **执行迁移** → 5. **验证结果**

## ⚡ 快速命令

```bash
# 一键检查迁移状态
source .venv/bin/activate && alembic current

# 一键查看所有表
sqlite3 app.db ".tables"

# 一键回滚最后一次迁移（如果需要）
source .venv/bin/activate && alembic downgrade -1
```

## ❗ 重要注意事项

1. **每次添加新模型后，必须在 `migrations/env.py` 中导入**
2. **先生成迁移文件，检查无误后再执行**
3. **保持模型文件的命名规范：model_name.py**
4. **迁移描述要清晰明确**