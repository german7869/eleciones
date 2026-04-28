#!/bin/sh
set -e

echo "Ejecutando migraciones y creando usuario administrador..."
python create_admin.py

echo "Iniciando servidor..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
