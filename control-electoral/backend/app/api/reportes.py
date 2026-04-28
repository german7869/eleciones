from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Voto, Candidato, Partido, Parroquia, Zona, Recinto, Junta, ResumenJunta
from app.utils.db import get_db
import openpyxl
import io

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/excel")
def exportar_excel(db: Session = Depends(get_db)):
    wb = openpyxl.Workbook()

    # Hoja 1: Resultados por candidato
    ws1 = wb.active
    ws1.title = "Resultados"
    ws1.append(["Candidato", "Partido", "Total Votos"])
    rows = (
        db.query(
            Candidato.nombre,
            Partido.nombre,
            func.coalesce(func.sum(Voto.nro_votos), 0)
        )
        .join(Partido, Candidato.partido_id == Partido.id)
        .outerjoin(Voto, Voto.candidato_id == Candidato.id)
        .group_by(Candidato.id, Candidato.nombre, Partido.nombre)
        .order_by(Candidato.orden_papeleta)
        .all()
    )
    for r in rows:
        ws1.append(list(r))

    # Hoja 2: Resumen por parroquia
    ws2 = wb.create_sheet("Por Parroquia")
    ws2.append(["Parroquia", "Votos Válidos", "Votos Nulos", "Votos Blancos", "Total Votantes"])
    parroquias = db.query(Parroquia).all()
    for p in parroquias:
        zona_ids = db.query(Zona.id).filter(Zona.parroquia_id == p.id).subquery()
        recinto_ids = db.query(Recinto.id).filter(Recinto.zona_id.in_(zona_ids)).subquery()
        junta_ids = db.query(Junta.id).filter(Junta.recinto_id.in_(recinto_ids)).subquery()
        validos = db.query(func.coalesce(func.sum(Voto.nro_votos), 0)).filter(Voto.junta_id.in_(junta_ids)).scalar()
        res = db.query(
            func.coalesce(func.sum(ResumenJunta.votos_nulos), 0),
            func.coalesce(func.sum(ResumenJunta.votos_blancos), 0),
            func.coalesce(func.sum(ResumenJunta.total_votantes), 0),
        ).filter(ResumenJunta.junta_id.in_(junta_ids)).first()
        ws2.append([p.nombre, validos, res[0], res[1], res[2]])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=resultados_electorales.xlsx"}
    )
