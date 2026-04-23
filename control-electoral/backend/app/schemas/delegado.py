from pydantic import BaseModel
from typing import Optional

class DelegadoBase(BaseModel):
    nombre: str
    cedula: str
    telefono: Optional[str] = None

class DelegadoCreate(DelegadoBase):
    pass

class DelegadoRead(DelegadoBase):
    id: int
    class Config:
        orm_mode = True
