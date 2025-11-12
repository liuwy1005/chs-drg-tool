from sqlalchemy import Column, String
from models.database import Base

class Exclude(Base):
    __tablename__ = 'Exclude'
    tb = Column(String(50), primary_key=True, nullable=False)
    maindiag = Column(String(50), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<Exclude(tb='{self.tb}', maindiag='{self.maindiag}')>"