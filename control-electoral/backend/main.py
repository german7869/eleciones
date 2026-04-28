from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import (
    parroquia, zona, recinto, junta, delegado,
    partido_candidato, voto_acta, auth, import_csv,
    encerar, upload_acta, resultados, dashboard, reportes, ejemplos,
    junta_delegado
)

app = FastAPI(title="Sistema de Control Electoral")

# Configurar CORS desde variable de entorno o valores por defecto
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.include_router(parroquia.router)
app.include_router(zona.router)
app.include_router(recinto.router)
app.include_router(junta_delegado.router)
app.include_router(junta.router)
app.include_router(delegado.router)
app.include_router(partido_candidato.router)
app.include_router(voto_acta.router)
app.include_router(auth.router)
app.include_router(import_csv.router)
app.include_router(ejemplos.router)
app.include_router(encerar.router)
app.include_router(upload_acta.router)
app.include_router(resultados.router)
app.include_router(dashboard.router)
app.include_router(reportes.router)

@app.get("/")
def read_root():
    return {"message": "Sistema de Control Electoral - Backend FastAPI"}
