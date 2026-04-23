from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import RecintoCreate, RecintoRead
from app.models import Recinto, Zona
from app.utils.db import get_db

router = APIRouter(prefix="/recintos", tags=["Recintos"])

@router.post("/", response_model=RecintoRead)
def create_recinto(recinto: RecintoCreate, db: Session = Depends(get_db)):
    zona = db.query(Zona).filter(Zona.id == recinto.zona_id).first()
    if not zona:
        raise HTTPException(status_code=422, detail="Zona no existe")
    db_recinto = Recinto(**recinto.dict())
    db.add(db_recinto)
    db.commit()
    db.refresh(db_recinto)
    return db_recinto

@router.get("/", response_model=list[RecintoRead])
def list_recintos(db: Session = Depends(get_db)):
    return db.query(Recinto).all()

@router.get("/{recinto_id}", response_model=RecintoRead)
def get_recinto(recinto_id: int, db: Session = Depends(get_db)):
    recinto = db.query(Recinto).filter(Recinto.id == recinto_id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    return recinto
