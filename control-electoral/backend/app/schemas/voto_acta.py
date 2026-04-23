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
