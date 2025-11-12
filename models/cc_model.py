from sqlalchemy import Column, Integer, String, Text
from models.database import Base

class CC(Base):
    """
    （并发症）数据模型
    """
    __tablename__ = 'CC' 

    diagcode = Column(String(50), primary_key=True, index=True)
    tb = Column(String(50), unique=True, index=True, nullable=False)  
    cctype = Column(String(100), nullable=False)  
    ccl = Column(Integer, nullable=False)  

    def __repr__(self):
        return f"<CC(diagcode='{self.diagcode}', tb='{self.tb}', cctype='{self.cctype}', ccl={self.ccl})>"