from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.db import Base

class Delegado(Base):
    __tablename__ = "delegados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cedula = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    password = Column(String, nullable=False, default="")
    rol = Column(String, nullable=False, default="delegado")  # "admin" | "delegado"
    juntas = relationship("Junta", backref="delegado")
