from sqlalchemy import Column, Integer, ForeignKey, String
from app.utils.db import Base

class Voto(Base):
    __tablename__ = "votos"
    id = Column(Integer, primary_key=True, index=True)
    junta_id = Column(Integer, ForeignKey("juntas.id"), nullable=False)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    nro_votos = Column(Integer, default=0)

class Acta(Base):
    __tablename__ = "actas"
    id = Column(Integer, primary_key=True, index=True)
    junta_id = Column(Integer, ForeignKey("juntas.id"), nullable=False)
    url_archivo = Column(String, nullable=False)

class ResumenJunta(Base):
    __tablename__ = "resumen_juntas"
    id = Column(Integer, primary_key=True, index=True)
    junta_id = Column(Integer, ForeignKey("juntas.id"), nullable=False, unique=True)
    votos_nulos = Column(Integer, default=0)
    votos_blancos = Column(Integer, default=0)
    total_votantes = Column(Integer, default=0)
