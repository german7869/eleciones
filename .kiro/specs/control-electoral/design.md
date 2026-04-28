# Sistema de Control Electoral — Diseño

## Arquitectura

```
Frontend (Vue 3 + TS)          Backend (FastAPI)           DB (PostgreSQL)
      │                               │                          │
      │  HTTP + JWT Bearer            │  SQLAlchemy ORM          │
      ├──────────────────────────────►│─────────────────────────►│
      │                               │                          │
   router.ts                      main.py                   tablas:
   views/                         app/api/                  parroquias
   components/                    app/models/               zonas
                                   app/schemas/              recintos
                                   app/services/             juntas
                                                             delegados
                                                             partidos
                                                             candidatos
                                                             votos
                                                             actas
```

## Cambios de modelo

### Delegado (agregar campo password)
```python
password = Column(String, nullable=False, default="")
rol = Column(String, default="delegado")  # "admin" | "delegado"
```

### Voto (agregar nulos/blancos)
Opción elegida: columnas adicionales en tabla `votos` por junta
```python
# Nueva tabla o columnas en Acta
class ResumenJunta(Base):
    junta_id: int (FK, unique)
    votos_nulos: int
    votos_blancos: int
    total_votantes: int
```

## Endpoints nuevos / modificados

| Método | Ruta | Descripción |
|--------|------|-------------|
| PUT | /parroquias/{id} | Actualizar parroquia |
| DELETE | /parroquias/{id} | Eliminar parroquia |
| PUT | /zonas/{id} | Actualizar zona |
| DELETE | /zonas/{id} | Eliminar zona |
| PUT | /recintos/{id} | Actualizar recinto |
| DELETE | /recintos/{id} | Eliminar recinto |
| PUT | /juntas/{id} | Actualizar junta |
| DELETE | /juntas/{id} | Eliminar junta |
| PUT | /delegados/{id} | Actualizar delegado |
| DELETE | /delegados/{id} | Eliminar delegado |
| PUT | /partidos/{id} | Actualizar partido |
| DELETE | /partidos/{id} | Eliminar partido |
| PUT | /partidos/candidatos/{id} | Actualizar candidato |
| DELETE | /partidos/candidatos/{id} | Eliminar candidato |
| GET | /resultados/ | Resultados agregados con filtros |
| POST | /import/zonas | Importar zonas CSV |
| POST | /import/recintos | Importar recintos CSV |
| POST | /import/juntas | Importar juntas CSV |
| POST | /votos/resumen/ | Guardar nulos/blancos por junta |
| GET | /votos/resumen/{junta_id} | Obtener resumen de junta |
| GET | /reportes/excel | Exportar Excel |

## Dependencias a agregar

### Backend (requirements.txt)
```
psycopg2-binary
openpyxl
```

### Frontend (package.json)
```json
"axios": "^1.6.0",
"chart.js": "^4.4.0",
"vue-chartjs": "^5.3.0"
```

## Seguridad
- Middleware de autenticación: función `get_current_user` con Depends
- Decorador de rol: `require_admin` para endpoints sensibles
- CORS: origins configurables por variable de entorno

## Estructura de vistas nuevas (frontend)
```
src/views/
  Admin/
    Delegados.vue       # CRUD delegados
    Parroquias.vue      # CRUD + import CSV
    Partidos.vue        # CRUD partidos y candidatos
  Dashboard.vue         # Home con estadísticas
```
