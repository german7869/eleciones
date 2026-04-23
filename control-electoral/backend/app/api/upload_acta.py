from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Junta, Acta
from app.utils.db import get_db
import os

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/upload", tags=["Subida de Actas"])

@router.post("/acta/{junta_id}")
def upload_acta(junta_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=415, detail="Formato no soportado")
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Archivo supera 10MB")
    junta = db.query(Junta).filter(Junta.id == junta_id).first()
    if not junta:
        raise HTTPException(status_code=404, detail="Junta no existe")
    ext = os.path.splitext(file.filename)[1]
    filename = f"acta_{junta_id}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    acta = Acta(junta_id=junta_id, url_archivo=filepath)
    db.add(acta)
    db.commit()
    db.refresh(acta)
    return {"url": filepath}
