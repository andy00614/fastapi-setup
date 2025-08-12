from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 1. 获取数据库连接字符串
DATABASE_URL = settings.DATABASE_URL  # "sqlite+aiosqlite:///./app.db"

# 2. 创建数据库引擎（连接器）
engine = create_async_engine(DATABASE_URL, echo=False)

# 3. 创建会话工厂（用来创建数据库会话）
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# 4. 获取数据库会话的函数
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session  # 这里应该是 yield，不是点号