from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import VotoCreate, VotoRead, ActaCreate, ActaRead, ResumenJuntaCreate, ResumenJuntaRead
from app.models import Voto, Acta, Junta, Candidato, ResumenJunta
from app.utils.db import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/votos", tags=["Votos y Actas"])

# --- Votos ---

@router.post("/", response_model=VotoRead)
def create_voto(voto: VotoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if not db.query(Junta).filter(Junta.id == voto.junta_id).first():
        raise HTTPException(status_code=422, detail="Junta no existe")
    if not db.query(Candidato).filter(Candidato.id == voto.candidato_id).first():
        raise HTTPException(status_code=422, detail="Candidato no existe")
    # Upsert: si ya existe el voto para esa junta+candidato, actualizar
    existing = db.query(Voto).filter(
        Voto.junta_id == voto.junta_id,
        Voto.candidato_id == voto.candidato_id
    ).first()
    if existing:
        existing.nro_votos = voto.nro_votos
        db.commit()
        db.refresh(existing)
        return existing
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

@router.get("/junta/{junta_id}", response_model=list[VotoRead])
def get_votos_por_junta(junta_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Obtener todos los votos de una junta"""
    junta = db.query(Junta).filter(Junta.id == junta_id).first()
    if not junta:
        raise HTTPException(status_code=404, detail="Junta no encontrada")
    
    votos = db.query(Voto).filter(Voto.junta_id == junta_id).all()
    return votos

# --- Resumen (nulos y blancos) ---

@router.post("/resumen/", response_model=ResumenJuntaRead)
def upsert_resumen(data: ResumenJuntaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if not db.query(Junta).filter(Junta.id == data.junta_id).first():
        raise HTTPException(status_code=422, detail="Junta no existe")
    existing = db.query(ResumenJunta).filter(ResumenJunta.junta_id == data.junta_id).first()
    if existing:
        existing.votos_nulos = data.votos_nulos
        existing.votos_blancos = data.votos_blancos
        existing.total_votantes = data.total_votantes
        db.commit()
        db.refresh(existing)
        return existing
    r = ResumenJunta(**data.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.get("/resumen/{junta_id}", response_model=ResumenJuntaRead)
def get_resumen(junta_id: int, db: Session = Depends(get_db)):
    r = db.query(ResumenJunta).filter(ResumenJunta.junta_id == junta_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resumen no encontrado para esta junta")
    return r

# --- Actas ---

@router.post("/actas/", response_model=ActaRead)
def create_acta(acta: ActaCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
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
