from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Partido(Base):
    __tablename__ = "partidos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    candidatos = relationship("Candidato", back_populates="partido")

class Candidato(Base):
    __tablename__ = "candidatos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=False)
    partido = relationship("Partido", back_populates="candidatos")
    orden_papeleta = Column(Integer, unique=True, nullable=False)
