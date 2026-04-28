from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ParroquiaCreate, ParroquiaRead
from app.models import Parroquia, Zona
from app.utils.db import get_db
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/parroquias", tags=["Parroquias"])

@router.post("/", response_model=ParroquiaRead)
def create_parroquia(parroquia: ParroquiaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db_p = Parroquia(**parroquia.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p

@router.get("/", response_model=list[ParroquiaRead])
def list_parroquias(db: Session = Depends(get_db)):
    return db.query(Parroquia).all()

@router.get("/{parroquia_id}", response_model=ParroquiaRead)
def get_parroquia(parroquia_id: int, db: Session = Depends(get_db)):
    p = db.query(Parroquia).filter(Parroquia.id == parroquia_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    return p

@router.put("/{parroquia_id}", response_model=ParroquiaRead)
def update_parroquia(parroquia_id: int, data: ParroquiaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.query(Parroquia).filter(Parroquia.id == parroquia_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    for k, v in data.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{parroquia_id}")
def delete_parroquia(parroquia_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Parroquia).filter(Parroquia.id == parroquia_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    if db.query(Zona).filter(Zona.parroquia_id == parroquia_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene zonas asociadas")
    db.delete(p)
    db.commit()
    return {"ok": True}
