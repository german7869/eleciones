from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import RecintoCreate, RecintoRead
from app.models import Recinto, Zona, Junta
from app.utils.db import get_db
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/recintos", tags=["Recintos"])

@router.post("/", response_model=RecintoRead)
def create_recinto(recinto: RecintoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if not db.query(Zona).filter(Zona.id == recinto.zona_id).first():
        raise HTTPException(status_code=422, detail="Zona no existe")
    db_r = Recinto(**recinto.dict())
    db.add(db_r)
    db.commit()
    db.refresh(db_r)
    return db_r

@router.get("/", response_model=list[RecintoRead])
def list_recintos(zona_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Recinto)
    if zona_id:
        q = q.filter(Recinto.zona_id == zona_id)
    return q.all()

@router.get("/{recinto_id}", response_model=RecintoRead)
def get_recinto(recinto_id: int, db: Session = Depends(get_db)):
    r = db.query(Recinto).filter(Recinto.id == recinto_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    return r

@router.put("/{recinto_id}", response_model=RecintoRead)
def update_recinto(recinto_id: int, data: RecintoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    r = db.query(Recinto).filter(Recinto.id == recinto_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    for k, v in data.dict().items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r

@router.delete("/{recinto_id}")
def delete_recinto(recinto_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    r = db.query(Recinto).filter(Recinto.id == recinto_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    if db.query(Junta).filter(Junta.recinto_id == recinto_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene juntas asociadas")
    db.delete(r)
    db.commit()
    return {"ok": True}
