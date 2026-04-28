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

### 2. Configurar variables de entorno (opcional)
```bash
cd /opt/control-electoral/backend
cp .env.example .env
# Editar .env si es necesario
```

### 3. Construir y levantar servicios
```bash
cd /opt/control-electoral
docker compose -f docker-compose.prod.yml up -d --build
```

### 4. Verificar despliegue
```bash
# Ver contenedores corriendo
docker ps

# Ver logs
docker logs control-electoral-frontend-1
docker logs control-electoral-backend-1
docker logs control-electoral-db-1

# Probar acceso
curl http://elecciones.sigecloud.com:8090
```

## Arquitectura

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
- CORS está configurado para elecciones.sigecloud.com:8090
- Para HTTPS, se requiere configurar certificados SSL (no incluido)

## Comandos útiles

```bash
# Reiniciar servicios
docker compose -f docker-compose.prod.yml restart

# Ver logs en tiempo real
docker compose -f docker-compose.prod.yml logs -f

# Detener servicios
docker compose -f docker-compose.prod.yml down

# Reconstruir después de cambios
docker compose -f docker-compose.prod.yml up -d --build
```
