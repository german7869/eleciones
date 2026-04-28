# Sistema de Control Electoral — Tareas de Implementación

- [x] 1. Corregir bugs críticos del backend
  - [x] 1.1 Agregar campo password y rol al modelo Delegado
  - [x] 1.2 Actualizar schemas DelegadoCreate y DelegadoRead
  - [x] 1.3 Agregar psycopg2-binary a requirements.txt y configurar CORS en main.py

- [x] 2. Corregir dependencias del frontend
  - [x] 2.1 Agregar axios, chart.js y vue-chartjs a package.json
  - [x] 2.2 Corregir BarChart.vue para usar vue-chartjs correctamente
  - [x] 2.3 Agregar interceptor de Axios en main.ts para JWT y manejo de 401

- [x] 3. Completar CRUD endpoints PUT y DELETE
  - [x] 3.1 Agregar PUT y DELETE en parroquia.py, zona.py, recinto.py
  - [x] 3.2 Agregar PUT y DELETE en junta.py, delegado.py, partido_candidato.py

- [x] 4. Implementar importacion CSV completa
  - [x] 4.1 Completar import_csv.py con logica real para parroquias, zonas, recintos y juntas

- [x] 5. Votos nulos y blancos
  - [x] 5.1 Crear modelo ResumenJunta y schemas correspondientes
  - [x] 5.2 Agregar endpoints POST y GET para resumen y actualizar encerar.py
  - [x] 5.3 Actualizar ReporteVotos.vue para persistir nulos y blancos

- [x] 6. Endpoint de resultados agregados en backend
  - [x] 6.1 Crear app/api/resultados.py con GET /resultados/ con filtros y agregacion en DB
  - [x] 6.2 Registrar router y refactorizar Resultados.vue para usar el nuevo endpoint

- [x] 7. Proteger endpoints con autenticacion JWT
  - [x] 7.1 Crear app/utils/auth.py con get_current_user y require_admin
  - [x] 7.2 Aplicar guards a endpoints de escritura y administracion

- [x] 8. Dashboard en Home.vue
  - [x] 8.1 Crear endpoint GET /dashboard/ con estadisticas generales
  - [x] 8.2 Reemplazar Home.vue con dashboard de tarjetas y barra de progreso

- [x] 9. Vistas de administracion frontend
  - [x] 9.1 Crear Admin/Delegados.vue, Admin/Partidos.vue, Admin/Territorios.vue
  - [x] 9.2 Agregar rutas admin en router.ts con guard de rol y enlaces en navbar

- [x] 10. Calidad y UX
  - [x] 10.1 Crear useToast.ts, Toast.vue y NotFound.vue
  - [x] 10.2 Agregar endpoint Excel, mejorar SubirActa.vue y ReporteVotos.vue con selector de junta
