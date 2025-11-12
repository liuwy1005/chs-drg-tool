from sqlalchemy import Column, String
from models.database import Base
class mdcdiagpool(Base):
    __tablename__ = 'AdrgMdcDiag'
    mdccode = Column(String(5), primary_key=True, index=True)
    diagcode = Column(String(50), primary_key=True, index=True)
    diagname = Column(String(300), nullable=True)
    submdc = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<MdcDiagPool(mdc_code='{self.mdc_code}', diagcode='{self.diagcode}', diagname='{self.diagname},submdc='{self.submdc}')>"