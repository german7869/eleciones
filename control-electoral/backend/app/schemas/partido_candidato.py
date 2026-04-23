from pydantic import BaseModel
from typing import Optional

class PartidoBase(BaseModel):
    codigo: str
    nombre: str

class PartidoCreate(PartidoBase):
    pass

class PartidoRead(PartidoBase):
    id: int
    class Config:
        orm_mode = True

class CandidatoBase(BaseModel):
    nombre: str
    partido_id: int
    orden_papeleta: int

class CandidatoCreate(CandidatoBase):
    pass

class CandidatoRead(CandidatoBase):
    id: int
    class Config:
        orm_mode = True
