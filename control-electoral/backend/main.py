from fastapi import FastAPI

from app.api import parroquia, zona, recinto, junta, delegado, partido_candidato, voto_acta, auth, import_csv, encerar, upload_acta

app = FastAPI()


app.include_router(parroquia.router)
app.include_router(zona.router)
app.include_router(recinto.router)
app.include_router(junta.router)
app.include_router(delegado.router)
app.include_router(partido_candidato.router)
app.include_router(voto_acta.router)
app.include_router(auth.router)
app.include_router(import_csv.router)
app.include_router(encerar.router)
app.include_router(upload_acta.router)

@app.get("/")
def read_root():
    return {"message": "Sistema de Control Electoral - Backend FastAPI"}
