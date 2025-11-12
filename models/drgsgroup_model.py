from sqlalchemy import Column, String, Numeric as Dec,Integer
from models.database import Base

class DrgsGroup(Base):
    """
    DRGS分组数据模型
    """
    __tablename__ = 'DrgsGroup'  # 指定数据库中的表名
    
    grpcode = Column(String(50), primary_key=True, index=True)
    grpname = Column(String(300), unique=True, index=True, nullable=False)
    iszz = Column(Integer, nullable=False)
    iscz = Column(Integer, nullable=True)
    isop = Column(String(1), nullable=False)
    rule = Column(String(100), nullable=True)
    paycw = Column(Dec(10,2), nullable=True)
    acode = Column(String(10), nullable=False)

    def __repr__(self):
        return f"<DrgsGroup(grpcode='{self.grpcode}', grpname='{self.grpname}', iszz='{self.iszz}', isop='{self.isop}', paycw='{self.paycw}', acode='{self.acode}')>"