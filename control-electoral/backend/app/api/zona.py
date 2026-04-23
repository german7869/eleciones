from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ZonaCreate, ZonaRead
from app.models import Zona, Parroquia
from app.utils.db import get_db

router = APIRouter(prefix="/zonas", tags=["Zonas"])

@router.post("/", response_model=ZonaRead)
def create_zona(zona: ZonaCreate, db: Session = Depends(get_db)):
    parroquia = db.query(Parroquia).filter(Parroquia.id == zona.parroquia_id).first()
    if not parroquia:
        raise HTTPException(status_code=422, detail="Parroquia no existe")
    db_zona = Zona(**zona.dict())
    db.add(db_zona)
    db.commit()
    db.refresh(db_zona)
    return db_zona

@router.get("/", response_model=list[ZonaRead])
def list_zonas(db: Session = Depends(get_db)):
    return db.query(Zona).all()

@router.get("/{zona_id}", response_model=ZonaRead)
def get_zona(zona_id: int, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    return zona
