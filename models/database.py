import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建基类
Base = declarative_base()

# 创建数据库引擎，连接SQLite数据库
engine = create_engine('sqlite:///./data/GroupConfig.db', echo=True)  # echo=True 用于显示SQL语句，生产环境可设为False

# 创建SessionLocal类，用于获取数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    依赖注入函数，用于在请求中获取数据库会话。
    使用完毕后会自动关闭会话。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """创建所有定义的表"""
    Base.metadata.create_all(bind=engine)