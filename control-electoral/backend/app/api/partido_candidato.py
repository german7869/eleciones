from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import PartidoCreate, PartidoRead, CandidatoCreate, CandidatoRead
from app.models import Partido, Candidato, Voto
from app.utils.db import get_db
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/partidos", tags=["Partidos y Candidatos"])

# --- Partidos ---

@router.post("/", response_model=PartidoRead)
def create_partido(partido: PartidoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Partido).filter(Partido.codigo == partido.codigo).first():
        raise HTTPException(status_code=422, detail="Código de partido ya registrado")
    db_p = Partido(**partido.dict())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p

@router.get("/", response_model=list[PartidoRead])
def list_partidos(db: Session = Depends(get_db)):
    return db.query(Partido).all()

@router.get("/{partido_id}", response_model=PartidoRead)
def get_partido(partido_id: int, db: Session = Depends(get_db)):
    p = db.query(Partido).filter(Partido.id == partido_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return p

@router.put("/{partido_id}", response_model=PartidoRead)
def update_partido(partido_id: int, data: PartidoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Partido).filter(Partido.id == partido_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    for k, v in data.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{partido_id}")
def delete_partido(partido_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(Partido).filter(Partido.id == partido_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    if db.query(Candidato).filter(Candidato.partido_id == partido_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene candidatos asociados")
    db.delete(p)
    db.commit()
    return {"ok": True}

# --- Candidatos ---

@router.post("/candidatos/", response_model=CandidatoRead)
def create_candidato(candidato: CandidatoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if not db.query(Partido).filter(Partido.id == candidato.partido_id).first():
        raise HTTPException(status_code=422, detail="Partido no existe")
    if db.query(Candidato).filter(Candidato.orden_papeleta == candidato.orden_papeleta).first():
        raise HTTPException(status_code=422, detail="Orden de papeleta ya asignado")
    db_c = Candidato(**candidato.dict())
    db.add(db_c)
    db.commit()
    db.refresh(db_c)
    return db_c

@router.get("/candidatos/", response_model=list[CandidatoRead])
def list_candidatos(db: Session = Depends(get_db)):
    return db.query(Candidato).all()

@router.get("/candidatos/{candidato_id}", response_model=CandidatoRead)
def get_candidato(candidato_id: int, db: Session = Depends(get_db)):
    c = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return c

@router.put("/candidatos/{candidato_id}", response_model=CandidatoRead)
def update_candidato(candidato_id: int, data: CandidatoCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    for k, v in data.dict().items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/candidatos/{candidato_id}")
def delete_candidato(candidato_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(Candidato).filter(Candidato.id == candidato_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    if db.query(Voto).filter(Voto.candidato_id == candidato_id).first():
        raise HTTPException(status_code=409, detail="No se puede eliminar: tiene votos registrados")
    db.delete(c)
    db.commit()
    return {"ok": True}
