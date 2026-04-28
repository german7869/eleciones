from pydantic import BaseModel
from typing import Optional

class DelegadoBase(BaseModel):
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    rol: Optional[str] = "delegado"

class DelegadoCreate(DelegadoBase):
    password: str

class DelegadoRead(DelegadoBase):
    id: int
    class Config:
        orm_mode = True

class CambiarClaveRequest(BaseModel):
    nueva_clave: str
