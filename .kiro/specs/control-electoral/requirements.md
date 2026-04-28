# Sistema de Control Electoral — Requisitos

## Contexto
Aplicación web para gestión y seguimiento de resultados electorales. Stack: FastAPI + PostgreSQL (backend), Vue 3 + TypeScript + Tailwind (frontend).

## Estado actual
- Modelos SQLAlchemy completos: Parroquia → Zona → Recinto → Junta, Delegado, Partido, Candidato, Voto, Acta
- CRUD básico (solo GET/POST) para todas las entidades
- Autenticación JWT por cédula/contraseña (bug: campo `password` falta en modelo Delegado)
- Frontend: Login, Resultados con filtros, ReporteVotos, SubirActa
- Import CSV: esqueleto sin lógica real
- Votos nulos/blancos: campos en frontend pero no se persisten

## Requisitos funcionales

### RF-01: Corrección de bugs críticos
- El modelo `Delegado` debe incluir campo `password` (hash bcrypt)
- El endpoint `/auth/login` debe funcionar correctamente
- El frontend debe enviar el token JWT en todas las peticiones autenticadas
- `axios` y `chart.js` deben estar en `package.json` (actualmente faltan)

### RF-02: Completar operaciones CRUD
- Endpoints PUT y DELETE para: Parroquia, Zona, Recinto, Junta, Delegado, Partido, Candidato
- Validaciones de integridad referencial al eliminar (no eliminar si tiene hijos)

### RF-03: Importación CSV completa
- Endpoint `/import/parroquias` debe insertar/actualizar registros reales desde CSV
- Endpoints similares para zonas, recintos y juntas
- Validación de columnas requeridas y manejo de errores por fila

### RF-04: Votos nulos y blancos
- Modelo `Voto` o tabla separada para registrar votos nulos y blancos por junta
- Backend: endpoint para guardar/consultar nulos y blancos
- Frontend `ReporteVotos.vue`: persistir nulos y blancos al enviar reporte

### RF-05: Endpoint de resultados agregados
- GET `/resultados/` con parámetros opcionales: `parroquia_id`, `zona_id`, `recinto_id`
- Retorna votos totales por candidato ya filtrados en el backend (no en frontend)
- Incluye totales de nulos, blancos y participación

### RF-06: Gestión de delegados (frontend)
- Vista para listar, crear, editar y eliminar delegados
- Asignación de delegado a junta desde la vista de juntas

### RF-07: Panel de administración territorial
- Vistas CRUD para Parroquia, Zona, Recinto, Junta (solo admin)
- Importación masiva desde CSV con preview y confirmación

### RF-08: Seguridad y roles
- Campo `rol` en Delegado: `admin` o `delegado`
- Endpoints de escritura protegidos con token JWT
- Endpoints de administración solo accesibles para rol `admin`
- CORS configurado correctamente en FastAPI

### RF-09: Exportación de reportes
- Endpoint GET `/reportes/excel` que genere archivo Excel con resultados
- Endpoint GET `/reportes/pdf` con resumen de resultados por parroquia

### RF-10: UX y calidad frontend
- Manejo de errores global con notificaciones (toast)
- Indicadores de carga en todas las peticiones
- Página 404 y manejo de sesión expirada (redirect a login)
- Home.vue con dashboard: totales de juntas reportadas, votos ingresados, actas subidas
