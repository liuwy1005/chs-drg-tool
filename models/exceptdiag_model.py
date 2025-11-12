from sqlalchemy import Column, String
from models.database import Base

class ExceptDiag(Base):
    """
    不应该编码的诊断数据模型
    """
    __tablename__ = 'ExceptDiag'  # 指定数据库中的表名
    
    diagcode = Column(String(50), primary_key=True, index=True)
    diagname = Column(String(200), unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"<ExceptDiag(diagcode='{self.diagcode}', diagname='{self.diagname}')>"