from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Junta, Acta, Voto, ResumenJunta
from app.utils.db import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):
    juntas_total = db.query(func.count(Junta.id)).scalar() or 0

    # Juntas que tienen al menos un voto > 0 registrado
    juntas_reportadas = (
        db.query(func.count(func.distinct(Voto.junta_id)))
        .filter(Voto.nro_votos > 0)
        .scalar() or 0
    )

    actas_subidas = db.query(func.count(Acta.id)).scalar() or 0

    total_votos = db.query(func.coalesce(func.sum(Voto.nro_votos), 0)).scalar() or 0

    total_nulos = db.query(func.coalesce(func.sum(ResumenJunta.votos_nulos), 0)).scalar() or 0
    total_blancos = db.query(func.coalesce(func.sum(ResumenJunta.votos_blancos), 0)).scalar() or 0

    progreso_pct = round(juntas_reportadas / juntas_total * 100, 1) if juntas_total > 0 else 0

    return {
        "juntas_total": juntas_total,
        "juntas_reportadas": juntas_reportadas,
        "actas_subidas": actas_subidas,
        "total_votos": total_votos,
        "total_nulos": total_nulos,
        "total_blancos": total_blancos,
        "progreso_pct": progreso_pct,
    }
