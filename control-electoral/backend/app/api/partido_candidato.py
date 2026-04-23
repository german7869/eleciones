from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import PartidoCreate, PartidoRead, CandidatoCreate, CandidatoRead
from app.models import Partido, Candidato
from app.utils.db import get_db

router = APIRouter(prefix="/partidos", tags=["Partidos y Candidatos"])

@router.post("/", response_model=PartidoRead)
def create_partido(partido: PartidoCreate, db: Session = Depends(get_db)):
    if db.query(Partido).filter(Partido.codigo == partido.codigo).first():
        raise HTTPException(status_code=422, detail="Código de partido ya registrado")
    db_partido = Partido(**partido.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

@router.get("/", response_model=list[PartidoRead])
def list_partidos(db: Session = Depends(get_db)):
    return db.query(Partido).all()

@router.get("/{partido_id}", response_model=PartidoRead)
def get_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = db.query(Partido).filter(Partido.id == partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@router.post("/candidatos/", response_model=CandidatoRead)
def create_candidato(candidato: CandidatoCreate, db: Session = Depends(get_db)):
    if not db.query(Partido).filter(Partido.id == candidato.partido_id).first():
        raise HTTPException(status_code=422, detail="Partido no existe")
    if db.query(Candidato).filter(Candidato.orden_papeleta == candidato.orden_papeleta).first():
        raise HTTPException(status_code=422, detail="Orden de papeleta ya asignado")
    db_candidato = Candidato(**candidato.dict())
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato

@router.get("/candidatos/", response_model=list[CandidatoRead])
def list_candidatos(db: Session = Depends(get_db)):
    return db.query(Candidato).all()

@router.get("/candidatos/{candidato_id}", response_model=CandidatoRead)
def get_candidato(candidato_id: int, db: Session = Depends(get_db)):
    candidato = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidato
