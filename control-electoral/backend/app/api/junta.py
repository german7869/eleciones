from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import JuntaCreate, JuntaRead
from app.models import Junta, Recinto, Delegado, Voto
from app.utils.db import get_db
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/juntas", tags=["Juntas"])

@router.post("/", response_model=JuntaRead)
def create_junta(junta: JuntaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if not db.query(Recinto).filter(Recinto.id == junta.recinto_id).first():
        raise HTTPException(status_code=422, detail="Recinto no existe")
    if junta.delegado_id and not db.query(Delegado).filter(Delegado.id == junta.delegado_id).first():
        raise HTTPException(status_code=422, detail="Delegado no existe")
    db_j = Junta(**junta.dict())
    db.add(db_j)
    db.commit()
    db.refresh(db_j)
    return db_j

@router.get("/", response_model=list[JuntaRead])
def list_juntas(recinto_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Junta)
    if recinto_id:
        q = q.filter(Junta.recinto_id == recinto_id)
    return q.all()

@router.get("/{junta_id}", response_model=JuntaRead)
def get_junta(junta_id: int, db: Session = Depends(get_db)):
    j = db.query(Junta).filter(Junta.id == junta_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    return j

@router.put("/{junta_id}", response_model=JuntaRead)
def update_junta(junta_id: int, data: JuntaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    j = db.query(Junta).filter(Junta.id == junta_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    for k, v in data.dict().items():
        setattr(j, k, v)
    db.commit()
    db.refresh(j)
    return j

@router.delete("/{junta_id}")
def delete_junta(junta_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    j = db.query(Junta).filter(Junta.id == junta_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    if db.query(Voto).filter(Voto.junta_id == junta_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene votos registrados")
    db.delete(j)
    db.commit()
    return {"ok": True}


@router.post("/{junta_id}/asignar-delegado")
def asignar_delegado(junta_id: int, data: dict, db: Session = Depends(get_db), _=Depends(require_admin)):
    """Asignar un delegado a una junta"""
    j = db.query(Junta).filter(Junta.id == junta_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    
    delegado_id = data.get("delegado_id")
    if not delegado_id:
        raise HTTPException(status_code=422, detail="delegado_id requerido")
    
    delegado = db.query(Delegado).filter(Delegado.id == delegado_id).first()
    if not delegado:
        raise HTTPException(status_code=404, detail="Delegado no encontrado")
    
    j.delegado_id = delegado_id
    db.commit()
    db.refresh(j)
    return {"ok": True, "message": f"Junta {j.nombre} asignada a {delegado.nombre}"}


@router.post("/{junta_id}/desasignar-delegado")
def desasignar_delegado(junta_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    """Desasignar delegado de una junta"""
    j = db.query(Junta).filter(Junta.id == junta_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    
    j.delegado_id = None
    db.commit()
    db.refresh(j)
    return {"ok": True, "message": f"Junta {j.nombre} desasignada"}


@router.post("/{junta_id}/marcar-procesada")
def marcar_procesada(junta_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    """Marcar una junta como procesada por el delegado"""
    j = db.query(Junta).filter(Junta.id == junta_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    
    j.estado = "procesada"
    db.commit()
    db.refresh(j)
    return {"ok": True, "message": f"Junta {j.nombre} marcada como procesada"}
