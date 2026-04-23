from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import DelegadoCreate, DelegadoRead
from app.models import Delegado
from app.utils.db import get_db

router = APIRouter(prefix="/delegados", tags=["Delegados"])

@router.post("/", response_model=DelegadoRead)
def create_delegado(delegado: DelegadoCreate, db: Session = Depends(get_db)):
    if db.query(Delegado).filter(Delegado.cedula == delegado.cedula).first():
        raise HTTPException(status_code=422, detail="Cédula ya registrada")
    db_delegado = Delegado(**delegado.dict())
    db.add(db_delegado)
    db.commit()
    db.refresh(db_delegado)
    return db_delegado

@router.get("/", response_model=list[DelegadoRead])
def list_delegados(db: Session = Depends(get_db)):
    return db.query(Delegado).all()

@router.get("/{delegado_id}", response_model=DelegadoRead)
def get_delegado(delegado_id: int, db: Session = Depends(get_db)):
    delegado = db.query(Delegado).filter(Delegado.id == delegado_id).first()
    if not delegado:
        raise HTTPException(status_code=404, detail="Delegado no encontrado")
    return delegado
