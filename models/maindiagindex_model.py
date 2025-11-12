from sqlalchemy import Column, String,Integer
from models.database import Base
class MainDiagIndex(Base):
    __tablename__ = 'MainDiagIndex'
    acode = Column(String(10), primary_key=True, index=True)
    diagcode = Column(String(50), primary_key=True, index=True)
    diagname = Column(String(300), nullable=True)
    grpno = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<MainDiagIndex(acode='{self.acode}', diagcode='{self.diagcode}', diagname='{self.diagname}', grpno='{self.grpno}')>"