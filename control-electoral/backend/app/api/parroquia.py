from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ParroquiaCreate, ParroquiaRead
from app.models import Parroquia
from app.utils.db import get_db

router = APIRouter(prefix="/parroquias", tags=["Parroquias"])

@router.post("/", response_model=ParroquiaRead)
def create_parroquia(parroquia: ParroquiaCreate, db: Session = Depends(get_db)):
    db_parroquia = Parroquia(**parroquia.dict())
    db.add(db_parroquia)
    db.commit()
    db.refresh(db_parroquia)
    return db_parroquia

@router.get("/", response_model=list[ParroquiaRead])
def list_parroquias(db: Session = Depends(get_db)):
    return db.query(Parroquia).all()

@router.get("/{parroquia_id}", response_model=ParroquiaRead)
def get_parroquia(parroquia_id: int, db: Session = Depends(get_db)):
    parroquia = db.query(Parroquia).filter(Parroquia.id == parroquia_id).first()
    if not parroquia:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    return parroquia
