from sqlalchemy import Column, Integer, String
from models.database import Base

class ADRG(Base):
    """
    ADRG（并发症）数据模型
    """
    __tablename__ = 'Adrg'  # 指定数据库中的表名

    # 定义字段，请根据你的adrg表实际列进行调整
    AdrgCode = Column(Integer, primary_key=True, index=True)
    AdrgName = Column(String(50), unique=True, index=True, nullable=False)  
    ScdLetter = Column(String(100), nullable=False)  
    Dept = Column(String(100), nullable=False)  

    def __repr__(self):
        return f"<ADRG(AdrgCode='{self.AdrgCode}', AdrgName='{self.AdrgName}, ScdLetter='{self.ScdLetter}', Dept='{self.Dept}')>"