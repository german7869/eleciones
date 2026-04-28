from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ZonaCreate, ZonaRead
from app.models import Zona, Parroquia, Recinto
from app.utils.db import get_db
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/zonas", tags=["Zonas"])

@router.post("/", response_model=ZonaRead)
def create_zona(zona: ZonaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if not db.query(Parroquia).filter(Parroquia.id == zona.parroquia_id).first():
        raise HTTPException(status_code=422, detail="Parroquia no existe")
    db_zona = Zona(**zona.dict())
    db.add(db_zona)
    db.commit()
    db.refresh(db_zona)
    return db_zona

@router.get("/", response_model=list[ZonaRead])
def list_zonas(parroquia_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Zona)
    if parroquia_id:
        q = q.filter(Zona.parroquia_id == parroquia_id)
    return q.all()

@router.get("/{zona_id}", response_model=ZonaRead)
def get_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona

@router.put("/{zona_id}", response_model=ZonaRead)
def update_zona(zona_id: int, data: ZonaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    for k, v in data.dict().items():
        setattr(zona, k, v)
    db.commit()
    db.refresh(zona)
    return zona

@router.delete("/{zona_id}")
def delete_zona(zona_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    if db.query(Recinto).filter(Recinto.zona_id == zona_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene recintos asociados")
    db.delete(zona)
    db.commit()
    return {"ok": True}
