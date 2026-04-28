from pydantic import BaseModel
from typing import Optional

class VotoBase(BaseModel):
    junta_id: int
    candidato_id: int
    nro_votos: int

class VotoCreate(VotoBase):
    pass

class VotoRead(VotoBase):
    id: int
    class Config:
        orm_mode = True

class ActaBase(BaseModel):
    junta_id: int
    url_archivo: str

class ActaCreate(ActaBase):
    pass

class ActaRead(ActaBase):
    id: int
    class Config:
        orm_mode = True

class ResumenJuntaBase(BaseModel):
    junta_id: int
    votos_nulos: int = 0
    votos_blancos: int = 0
    total_votantes: int = 0

class ResumenJuntaCreate(ResumenJuntaBase):
    pass

class ResumenJuntaRead(ResumenJuntaBase):
    id: int
    class Config:
        orm_mode = True
