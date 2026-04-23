from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Delegado(Base):
    __tablename__ = "delegados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    juntas = relationship("Junta", backref="delegado")
