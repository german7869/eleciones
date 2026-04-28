from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.models import Voto, Candidato, Partido, Junta, Recinto, Zona, ResumenJunta
from app.utils.db import get_db

router = APIRouter(prefix="/resultados", tags=["Resultados"])

@router.get("/")
def get_resultados(
    parroquia_id: Optional[int] = None,
    zona_id: Optional[int] = None,
    recinto_id: Optional[int] = None,
    junta_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Construir subquery de junta_ids según filtros
    junta_query = db.query(Junta.id)
    if junta_id:
        junta_query = junta_query.filter(Junta.id == junta_id)
    elif recinto_id:
        junta_query = junta_query.filter(Junta.recinto_id == recinto_id)
    elif zona_id:
        recinto_ids = db.query(Recinto.id).filter(Recinto.zona_id == zona_id).subquery()
        junta_query = junta_query.filter(Junta.recinto_id.in_(recinto_ids))
    elif parroquia_id:
        zona_ids = db.query(Zona.id).filter(Zona.parroquia_id == parroquia_id).subquery()
        recinto_ids = db.query(Recinto.id).filter(Recinto.zona_id.in_(zona_ids)).subquery()
        junta_query = junta_query.filter(Junta.recinto_id.in_(recinto_ids))

    junta_ids = junta_query.subquery()

    # Votos por candidato
    votos_por_candidato = (
        db.query(
            Candidato.id.label("candidato_id"),
            Candidato.nombre.label("candidato"),
            Partido.nombre.label("partido"),
            func.coalesce(func.sum(Voto.nro_votos), 0).label("total_votos"),
        )
        .join(Partido, Candidato.partido_id == Partido.id)
        .outerjoin(Voto, (Voto.candidato_id == Candidato.id) & (Voto.junta_id.in_(junta_ids)))
        .group_by(Candidato.id, Candidato.nombre, Partido.nombre)
        .order_by(Candidato.orden_papeleta)
        .all()
    )

    total_validos = sum(r.total_votos for r in votos_por_candidato)

    # Totales de nulos y blancos
    resumen_totals = (
        db.query(
            func.coalesce(func.sum(ResumenJunta.votos_nulos), 0).label("nulos"),
            func.coalesce(func.sum(ResumenJunta.votos_blancos), 0).label("blancos"),
            func.coalesce(func.sum(ResumenJunta.total_votantes), 0).label("votantes"),
        )
        .filter(ResumenJunta.junta_id.in_(junta_ids))
        .first()
    )

    nulos = resumen_totals.nulos if resumen_totals else 0
    blancos = resumen_totals.blancos if resumen_totals else 0
    total_votantes = resumen_totals.votantes if resumen_totals else 0
    total_emitidos = total_validos + nulos + blancos
    participacion = round(total_emitidos / total_votantes * 100, 2) if total_votantes > 0 else 0

    candidatos_result = []
    for r in votos_por_candidato:
        pct = round(r.total_votos / total_emitidos * 100, 2) if total_emitidos > 0 else 0
        candidatos_result.append({
            "candidato_id": r.candidato_id,
            "candidato": r.candidato,
            "partido": r.partido,
            "total_votos": r.total_votos,
            "porcentaje": pct,
        })

    return {
        "candidatos": candidatos_result,
        "totales": {
            "votos_validos": total_validos,
            "votos_nulos": nulos,
            "votos_blancos": blancos,
            "total_emitidos": total_emitidos,
            "total_votantes": total_votantes,
            "participacion_pct": participacion,
        }
    }
