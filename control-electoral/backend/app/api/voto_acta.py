from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import VotoCreate, VotoRead, ActaCreate, ActaRead
from app.models import Voto, Acta, Junta, Candidato
from app.utils.db import get_db

router = APIRouter(prefix="/votos", tags=["Votos y Actas"])

@router.post("/", response_model=VotoRead)
def create_voto(voto: VotoCreate, db: Session = Depends(get_db)):
    if not db.query(Junta).filter(Junta.id == voto.junta_id).first():
        raise HTTPException(status_code=422, detail="Junta no existe")
    if not db.query(Candidato).filter(Candidato.id == voto.candidato_id).first():
        raise HTTPException(status_code=422, detail="Candidato no existe")
    db_voto = Voto(**voto.dict())
    db.add(db_voto)
    db.commit()
    db.refresh(db_voto)
    return db_voto

@router.get("/", response_model=list[VotoRead])
def list_votos(db: Session = Depends(get_db)):
    return db.query(Voto).all()

@router.get("/{voto_id}", response_model=VotoRead)
def get_voto(voto_id: int, db: Session = Depends(get_db)):
    voto = db.query(Voto).filter(Voto.id == voto_id).first()
    if not voto:
        raise HTTPException(status_code=404, detail="Voto no encontrado")
    return voto

@router.post("/actas/", response_model=ActaRead)
def create_acta(acta: ActaCreate, db: Session = Depends(get_db)):
    if not db.query(Junta).filter(Junta.id == acta.junta_id).first():
        raise HTTPException(status_code=422, detail="Junta no existe")
    db_acta = Acta(**acta.dict())
    db.add(db_acta)
    db.commit()
    db.refresh(db_acta)
    return db_acta

@router.get("/actas/", response_model=list[ActaRead])
def list_actas(db: Session = Depends(get_db)):
    return db.query(Acta).all()

@router.get("/actas/{acta_id}", response_model=ActaRead)
def get_acta(acta_id: int, db: Session = Depends(get_db)):
    acta = db.query(Acta).filter(Acta.id == acta_id).first()
    if not acta:
        raise HTTPException(status_code=404, detail="Acta no encontrada")
    return acta
