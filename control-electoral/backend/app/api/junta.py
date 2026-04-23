from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import JuntaCreate, JuntaRead
from app.models import Junta, Recinto, Delegado
from app.utils.db import get_db

router = APIRouter(prefix="/juntas", tags=["Juntas"])

@router.post("/", response_model=JuntaRead)
def create_junta(junta: JuntaCreate, db: Session = Depends(get_db)):
    recinto = db.query(Recinto).filter(Recinto.id == junta.recinto_id).first()
    if not recinto:
        raise HTTPException(status_code=422, detail="Recinto no existe")
    if junta.delegado_id:
        delegado = db.query(Delegado).filter(Delegado.id == junta.delegado_id).first()
        if not delegado:
            raise HTTPException(status_code=422, detail="Delegado no existe")
    db_junta = Junta(**junta.dict())
    db.add(db_junta)
    db.commit()
    db.refresh(db_junta)
    return db_junta

@router.get("/", response_model=list[JuntaRead])
def list_juntas(db: Session = Depends(get_db)):
    return db.query(Junta).all()

@router.get("/{junta_id}", response_model=JuntaRead)
def get_junta(junta_id: int, db: Session = Depends(get_db)):
    junta = db.query(Junta).filter(Junta.id == junta_id).first()
    if not junta:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    return junta
