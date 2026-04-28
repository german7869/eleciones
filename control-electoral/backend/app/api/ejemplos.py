from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import os

router = APIRouter(prefix="/ejemplos", tags=["Ejemplos"])

# Directorio donde están los archivos de ejemplo
EJEMPLOS_DIR = "/app"

@router.get("/{filename}")
def descargar_ejemplo(filename: str):
    """Descargar archivo de ejemplo CSV"""
    # Solo permitir descargas de archivos de ejemplo
    allowed_files = [
        "parroquias_ejemplo.csv",
        "zonas_ejemplo.csv",
        "recintos_ejemplo.csv",
        "juntas_ejemplo.csv"
    ]
    
    if filename not in allowed_files:
        raise HTTPException(status_code=400, detail="Archivo no permitido")
    
    file_path = os.path.join(EJEMPLOS_DIR, filename)
    
    # Validar que el archivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {filename}")
    
    # Retornar como descarga usando StreamingResponse
    def iterfile():
        with open(file_path, mode="rb") as file_like:
            yield from file_like
    
    return StreamingResponse(
        iterfile(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "text/csv; charset=utf-8"
        }
    )
