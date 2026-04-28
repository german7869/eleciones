from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.db import get_db
from app.utils.auth import require_admin, get_current_user
from app.models import Junta, Delegado

router = APIRouter(prefix="/juntas", tags=["Juntas"])

class AsignarDelegadoSchema(BaseModel):
    junta_id: int
    delegado_id: int | None = None  # None para deseleccionar

@router.post("/asignar-delegado")
def asignar_delegado(
    data: AsignarDelegadoSchema,
    db: Session = Depends(get_db),
    current_user: Delegado = Depends(require_admin)
):
    """Asignar un delegado a una junta (solo admin)"""
    
    junta = db.query(Junta).filter(Junta.id == data.junta_id).first()
    if not junta:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    
    if data.delegado_id:
        delegado = db.query(Delegado).filter(Delegado.id == data.delegado_id).first()
        if not delegado:
            raise HTTPException(status_code=404, detail="Delegado no encontrado")
        if delegado.rol != "delegado":
            raise HTTPException(status_code=400, detail="Solo se pueden asignar delegados (rol='delegado')")
        junta.delegado_id = delegado.id
    else:
        junta.delegado_id = None
    
    db.commit()
    return {
        "mensaje": "Delegado asignado correctamente" if data.delegado_id else "Delegado desasignado",
        "junta_id": junta.id,
        "junta_nombre": junta.nombre,
        "delegado_id": junta.delegado_id
    }

@router.get("/listar-juntas-sin-delegado")
def listar_juntas_sin_delegado(db: Session = Depends(get_db)):
    """Listar juntas sin delegado asignado - público"""
    juntas = db.query(Junta).filter(Junta.delegado_id == None).all()
    return [
        {
            "id": j.id,
            "codigo": j.codigo,
            "nombre": j.nombre,
            "recinto_nombre": j.recinto.nombre if j.recinto else "",
            "tipo": j.tipo.value if j.tipo else ""
        }
        for j in juntas
    ]

@router.get("/listar-delegados-disponibles")
def listar_delegados_disponibles(db: Session = Depends(get_db)):
    """Listar delegados disponibles para asignar - público"""
    delegados = db.query(Delegado).filter(Delegado.rol == "delegado").all()
    return [
        {
            "id": d.id,
            "nombre": d.nombre,
            "cedula": d.cedula,
            "juntas_asignadas": len(d.juntas)
        }
        for d in delegados
    ]

@router.get("/mis-juntas")
def mis_juntas(
    db: Session = Depends(get_db),
    current_user: Delegado = Depends(get_current_user)
):
    """Obtener juntas asignadas al delegado autenticado"""
    if current_user.rol == "admin":
        raise HTTPException(status_code=403, detail="Endpoint solo para delegados")
    
    juntas = db.query(Junta).filter(Junta.delegado_id == current_user.id).all()
    return [
        {
            "id": j.id,
            "codigo": j.codigo,
            "nombre": j.nombre,
            "recinto_nombre": j.recinto.nombre if j.recinto else "",
            "recinto_id": j.recinto_id,
            "tipo": j.tipo.value if j.tipo else "",
            "nro_votantes": j.nro_votantes
        }
        for j in juntas
    ]
