# Sistema de Control Electoral

Aplicación web para la gestión y control de procesos electorales con funcionalidades de votación, actas y reportes.

## Arquitectura

```
Internet (https://elecciones.sigecloud.com)
   │
   ▼
┌─────────────────────────────────────────────┐
│          Host Nginx (Reverse Proxy)          │
│          Puerto 443 (HTTPS)                  │
│                ↓                            │
│          localhost:8090                     │
└─────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────┐
│     Docker: Puerto 8090 (Host) → 80 (Container)    │
│                ↓                            │
│  Frontend Container (Nginx :80)         │
│    ├─ / → Vue.js App                      │
│    └─ /api → proxy to backend             │
│                ↓                            │
│  Backend Container (FastAPI :8000)        │
│                ↓                            │
│  DB Container (PostgreSQL :5432)           │
└─────────────────────────────────────────────┘
```

**Frontend** es el ÚNICO punto de acceso externo dentro de Docker. Backend y DB son servicios internos en red Docker.

**Nota:** El puerto 8090 de Docker es para comunicación interna del host. El usuario final accede vía HTTPS (puerto 443).

## Credenciales

Las credenciales del administrador se configuran en el archivo `backend/.env`:

```bash
# Copiar archivo de ejemplo
cd backend
cp .env.example .env

# Editar con tus credenciales
nano .env
```

**Credenciales por defecto** (solo si no se configura `.env`):

| Campo | Valor |
|-------|-------|
| Cédula/Email | `germandase@gmail.com` |
| Contraseña | `jedase7869` |
| Rol | `admin` |

**⚠️ IMPORTANTE:** Cambiar estas credenciales en producción editando `backend/.env` y recrear el contenedor:
```bash
docker compose up -d --build backend
```

## Despliegue en Producción

### Requisitos
- Docker y Docker Compose instalados
- Puerto 8090 disponible
- DNS configurado: `elecciones.sigecloud.com` apuntando a la IP del servidor

### Pasos

```bash
# 1. Ir al directorio
cd /home/orlock/Dev/eleciones/control-electoral

# 2. Construir y levantar servicios
docker compose up -d --build

# 3. Verificar que todo esté corriendo
docker ps

# 4. Ver logs si es necesario
docker compose logs -f
```

### Acceso
```
https://elecciones.sigecloud.com
```

**Nota:** El puerto 8090 es solo para comunicación interna entre el nginx del host y Docker. El usuario accede vía HTTPS (puerto 443).

## Desarrollo

```bash
# Base de datos
docker compose -f docker-compose.dev.yml up -d db

# Backend (con hot reload)
cd backend && uvicorn main:app --reload --port 8000

# Frontend (otra terminal)
cd frontend && npm run dev
```

## Servicios

| Servicio | Descripción | Puerto interno | Puerto externo |
|----------|-------------|----------------|---------------|
| frontend | Vue.js + Nginx (proxy a /api) | 80 | 8090 |
| backend | FastAPI | 8000 | - (solo red Docker) |
| db | PostgreSQL 17 | 5432 | - (solo red Docker) |

## Migraciones

En producción, las migraciones de base de datos se ejecutan **automáticamente** al iniciar el contenedor backend vía `entrypoint.sh`.

En desarrollo, ejecutar manualmente:
```bash
cd backend
python -c "from app.utils.init_db import init_db; init_db()"
```

## Comandos útiles

```bash
# Ver contenedores corriendo
docker ps

# Ver logs de un servicio específico
docker logs control-electoral-backend-1
docker logs control-electoral-frontend-1

# Reiniciar servicios
docker compose restart

# Detener todo
docker compose down

# Reconstruir después de cambios
docker compose up -d --build

# Eliminar volumen de base de datos (¡CUIDADO! borra todos los datos)
docker compose down -v
```

## Estructura del proyecto

```
control-electoral/
├── backend/
│   ├── app/                 # Código principal FastAPI
│   ├── Dockerfile           # Imagen del backend
│   ├── entrypoint.sh        # Migraciones + inicio
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/                 # Código Vue.js
│   ├── Dockerfile           # Build de producción
│   ├── nginx.conf           # Configuración nginx (puerto 8090 interno)
│   └── package.json
├── docker-compose.yml       # Producción (frontend :8090 en host)
├── docker-compose.dev.yml   # Desarrollo (puertos expuestos)
└── README.md
```

## Configuración de Nginx en el Host (HTTPS)

Para configurar el reverse proxy en el host con SSL:

1. Instalar certbot:
```bash
sudo apt-get install certbot python3-certbot-nginx -y
```

2. Generar certificado SSL:
```bash
sudo certbot --nginx -d elecciones.sigecloud.com
```

3. Copiar la configuración de nginx:
```bash
sudo cp host-nginx-elecciones.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/host-nginx-elecciones.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Tecnologías

- **Frontend:** Vue.js 3, TypeScript, Tailwind CSS, Vite, Chart.js
- **Backend:** FastAPI, Python 3.12, SQLAlchemy, Pydantic
- **Base de datos:** PostgreSQL 17
- **Web server:** Nginx (Alpine)
