# Despliegue de Control Electoral

## Requisitos
- Docker y Docker Compose instalados
- Puerto 8090 disponible en el servidor
- DNS configurado: elecciones.sigecloud.com apuntando a la IP del servidor

## Instrucciones de despliegue

### 1. Copiar archivos al servidor
```bash
scp -r control-electoral/ user@servidor:/opt/control-electoral/
```

### 2. Configurar variables de entorno
```bash
cd /opt/control-electoral/backend
cp .env.example .env
# Editar .env con tus credenciales
nano .env
```

### 3. Construir y levantar servicios
```bash
cd /opt/control-electoral
docker compose up -d --build
```

### 4. Verificar despliegue
```bash
# Ver contenedores corriendo
docker ps

# Ver logs
docker logs control-electoral-frontend-1
docker logs control-electoral-backend-1
docker logs control-electoral-db-1

# Probar acceso (vía nginx del host)
curl http://elecciones.sigecloud.com
```

## Arquitectura

```
Internet (http://elecciones.sigecloud.com)
   │
   ▼
┌─────────────────────────────┐
│  Host Nginx (Reverse Proxy) │
│  Puerto 80/443             │
│       ↓                     │
│  localhost:8090            │
└─────────────────────────────┘
   │
   ▼
┌─────────────────────────────┐
│  Docker: 8090→80 (Container) │
│  Frontend Container         │
│  (Nginx :80)             │
│    ├─ / → Vue.js app        │
│    └─ /api → proxy to      │
│              ↓              │
│  Backend Container          │
│  (FastAPI :8000)           │
│    ↓                        │
│  DB Container               │
│  (PostgreSQL :5432)        │
└─────────────────────────────┘
```
Internet
   │
   ▼
┌─────────────────────────────┐
│  Puerto 8090 (Host)        │
│  ↓                          │
│  Frontend Container         │
│  (Nginx :8090)             │
│    ├─ / → Vue.js app        │
│    └─ /api → proxy to      │
│              ↓              │
│  Backend Container          │
│  (FastAPI :8000)           │
│    ↓                        │
│  DB Container               │
│  (PostgreSQL :5432)        │
└─────────────────────────────┘
```

## Notas importantes

- El backend NO está expuesto al exterior, solo accesible vía el frontend
- La base de datos NO está expuesta, solo accesible por el backend
- CORS está configurado para elecciones.sigecloud.com (sin puerto, porque el usuario accede vía nginx en puerto 80/443)
- Las migraciones y usuario admin se crean automáticamente
- Para HTTPS, se requiere configurar certificados SSL (no incluido)
- El puerto 8090 es solo para comunicación interna: nginx (host) → frontend (Docker)

## Comandos útiles

```bash
# Reiniciar servicios
docker compose restart

# Ver logs en tiempo real
docker compose logs -f

# Detener servicios
docker compose down

# Reconstruir después de cambios
docker compose up -d --build
```
