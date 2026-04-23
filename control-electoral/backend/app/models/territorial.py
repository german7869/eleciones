from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class TipoJuntaEnum(str, enum.Enum):
    masculino = "m"
    femenino = "f"

class Parroquia(Base):
    __tablename__ = "parroquias"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    nro_juntas_masculino = Column(Integer, default=0)
    nro_juntas_femenino = Column(Integer, default=0)
    nro_votantes = Column(Integer, default=0)
    zonas = relationship("Zona", back_populates="parroquia")

class Zona(Base):
    __tablename__ = "zonas"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    parroquia_id = Column(Integer, ForeignKey("parroquias.id"), nullable=False)
    parroquia = relationship("Parroquia", back_populates="zonas")
    recintos = relationship("Recinto", back_populates="zona")

class Recinto(Base):
    __tablename__ = "recintos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=True)
    nro_juntas_masculino = Column(Integer, default=0)
    nro_juntas_femenino = Column(Integer, default=0)
    nro_votantes = Column(Integer, default=0)
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=False)
    zona = relationship("Zona", back_populates="recintos")
    juntas = relationship("Junta", back_populates="recinto")

class Junta(Base):
    __tablename__ = "juntas"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    recinto_id = Column(Integer, ForeignKey("recintos.id"), nullable=False)
    recinto = relationship("Recinto", back_populates="juntas")
    numero = Column(Integer, nullable=False)
    tipo = Column(Enum(TipoJuntaEnum), nullable=False)
    nro_votantes = Column(Integer, default=0)
    delegado_id = Column(Integer, ForeignKey("delegados.id"), nullable=True)
