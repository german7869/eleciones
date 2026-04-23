from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Junta, Candidato, Voto
from app.utils.db import get_db

router = APIRouter(prefix="/encerar", tags=["Encerar votos"])

@router.post("/")
def encerar(db: Session = Depends(get_db)):
    juntas = db.query(Junta).all()
    candidatos = db.query(Candidato).all()
    total = 0
    for junta in juntas:
        for candidato in candidatos:
            voto = db.query(Voto).filter_by(junta_id=junta.id, candidato_id=candidato.id).first()
            if voto:
                voto.nro_votos = 0
            else:
                voto = Voto(junta_id=junta.id, candidato_id=candidato.id, nro_votos=0)
                db.add(voto)
            total += 1
    db.commit()
    return {"msg": f"{total} votos inicializados"}
