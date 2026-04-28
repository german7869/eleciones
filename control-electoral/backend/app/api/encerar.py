from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Junta, Candidato, Voto, ResumenJunta
from app.utils.db import get_db
from app.utils.auth import require_admin

router = APIRouter(prefix="/encerar", tags=["Encerar votos"])

@router.post("/")
def encerar(db: Session = Depends(get_db), _=Depends(require_admin)):
    juntas = db.query(Junta).all()
    candidatos = db.query(Candidato).all()
    total_votos = 0
    for junta in juntas:
        for candidato in candidatos:
            voto = db.query(Voto).filter_by(junta_id=junta.id, candidato_id=candidato.id).first()
            if voto:
                voto.nro_votos = 0
            else:
                db.add(Voto(junta_id=junta.id, candidato_id=candidato.id, nro_votos=0))
            total_votos += 1
        # Resetear resumen de nulos/blancos
        resumen = db.query(ResumenJunta).filter_by(junta_id=junta.id).first()
        if resumen:
            resumen.votos_nulos = 0
            resumen.votos_blancos = 0
            resumen.total_votantes = 0
        else:
            db.add(ResumenJunta(junta_id=junta.id, votos_nulos=0, votos_blancos=0, total_votantes=0))
    db.commit()
    return {"msg": f"{total_votos} votos inicializados, {len(juntas)} resúmenes reseteados"}
