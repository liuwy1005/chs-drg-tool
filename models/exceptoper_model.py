from sqlalchemy import Column, String
from models.database import Base

class ExceptOper(Base):
    """
    不应该编码的手术数据模型
    """
    __tablename__ = 'ExceptOper'
    
    opercode = Column(String(50), primary_key=True, index=True)
    opername = Column(String(200), unique=True, index=True, nullable=False)

    def __repr__(self):
        return f"<ExceptOper(opercode='{self.opercode}', opername='{self.opername}')>"