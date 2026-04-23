from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
import pandas as pd

router = APIRouter(prefix="/import", tags=["Importación CSV"])

@router.post("/parroquias")
def import_parroquias(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    # Aquí iría la lógica de inserción/actualización
    return {"msg": f"{len(df)} parroquias procesadas"}

# Repetir para zonas, recintos, juntas según necesidad
