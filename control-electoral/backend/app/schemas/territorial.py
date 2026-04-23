from pydantic import BaseModel, Field
from typing import Optional, List

class ParroquiaBase(BaseModel):
    codigo: str
    nombre: str
    nro_juntas_masculino: Optional[int] = 0
    nro_juntas_femenino: Optional[int] = 0
    nro_votantes: Optional[int] = 0

class ParroquiaCreate(ParroquiaBase):
    pass

class ParroquiaRead(ParroquiaBase):
    id: int
    class Config:
        orm_mode = True

class ZonaBase(BaseModel):
    codigo: str
    nombre: str
    parroquia_id: int

class ZonaCreate(ZonaBase):
    pass

class ZonaRead(ZonaBase):
    id: int
    class Config:
        orm_mode = True

class RecintoBase(BaseModel):
    codigo: str
    nombre: str
    direccion: Optional[str] = None
    nro_juntas_masculino: Optional[int] = 0
    nro_juntas_femenino: Optional[int] = 0
    nro_votantes: Optional[int] = 0
    zona_id: int

class RecintoCreate(RecintoBase):
    pass

class RecintoRead(RecintoBase):
    id: int
    class Config:
        orm_mode = True

class JuntaBase(BaseModel):
    codigo: str
    nombre: str
    recinto_id: int
    numero: int
    tipo: str
    nro_votantes: Optional[int] = 0
    delegado_id: Optional[int] = None

class JuntaCreate(JuntaBase):
    pass

class JuntaRead(JuntaBase):
    id: int
    class Config:
        orm_mode = True
