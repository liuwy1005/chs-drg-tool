from sqlalchemy import Column, String,Integer
from models.database import Base
class MainSurgeryIndex(Base):
    __tablename__ = 'MainSurgeryIndex'
    acode = Column(String(10), primary_key=True, index=True)
    opercode = Column(String(50), primary_key=True, index=True)
    opername = Column(String(300), nullable=True)
    grpno = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<MainSurgeryIndex(acode='{self.acode}', opercode='{self.opercode}', opername='{self.opername}', grpno='{self.grpno}')>"