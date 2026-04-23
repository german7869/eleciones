from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
