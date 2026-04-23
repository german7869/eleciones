# Documento de Requisitos

## Introducción

El Sistema de Control Electoral es una plataforma compuesta por un backend REST (FastAPI), una aplicación web de resultados (Vue 3 + TailAdmin + Tailwind CSS v4 + TypeScript) y una aplicación móvil web-responsive para delegados. Permite gestionar la estructura territorial electoral (parroquias, zonas, recintos, juntas), importar datos desde CSV, asignar delegados a juntas, registrar votos reportados por cada junta y visualizar resultados en tiempo real con filtros y gráficas.

---

## Glosario

- **Sistema**: El Sistema de Control Electoral en su conjunto.
- **Backend**: Servicio REST implementado en FastAPI que expone todos los endpoints de la API.
- **App_Web**: Aplicación web de resultados construida con Vue 3, TailAdmin, Tailwind CSS v4 y TypeScript.
- **App_Movil**: Aplicación web responsive utilizada por los delegados para reportar votos.
- **Importador_CSV**: Módulo del Backend responsable de procesar archivos CSV y persistir los datos en la base de datos.
- **Parroquia**: Unidad territorial de nivel superior. Contiene zonas. Campos: `codigo`, `nombre`, `nro_juntas_masculino`, `nro_juntas_femenino`, `nro_votantes`.
- **Zona**: Unidad territorial de nivel intermedio. Pertenece a una Parroquia. Campos: `codigo`, `nombre`, `parroquia_id`.
- **Recinto**: Lugar físico de votación. Pertenece a una Zona. Campos: `codigo`, `nombre`, `direccion`, `nro_juntas_masculino`, `nro_juntas_femenino`, `nro_votantes`.
- **Junta**: Unidad mínima de votación. Pertenece a un Recinto. Campos: `codigo`, `nombre`, `recinto_id`, `numero`, `tipo` (`m`=masculino, `f`=femenino), `nro_votantes`, `delegado_id`.
- **Delegado**: Persona responsable de reportar los votos de una o más Juntas. Campos: `id`, `nombre`, `cedula`, `telefono`.
- **Partido**: Organización política. Campos: `id`, `codigo`, `nombre`.
- **Candidato**: Persona que compite en la elección. Pertenece a un Partido. Campos: `id`, `nombre`, `partido_id`, `orden_papeleta`.
- **Voto**: Registro de votos de un Candidato en una Junta. Campos: `id`, `junta_id`, `candidato_id`, `nro_votos`.
- **Acta**: Imagen del documento físico de resultados de una Junta.
- **Encerar**: Operación que inicializa todos los registros de Votos con `nro_votos = 0` para cada combinación de Junta y Candidato existente.
- **Jerarquía_Territorial**: Estructura Parroquia → Zona → Recinto → Junta.

---

## Requisitos

### Requisito 1: Modelo de datos territorial

**User Story:** Como administrador del sistema, quiero que la estructura territorial (parroquias, zonas, recintos, juntas) esté correctamente modelada, para que todos los demás módulos puedan referenciarla de forma consistente.

#### Criterios de Aceptación

1. THE Backend SHALL almacenar Parroquias con los campos `codigo` (único), `nombre`, `nro_juntas_masculino`, `nro_juntas_femenino` y `nro_votantes`.
2. THE Backend SHALL almacenar Zonas con los campos `codigo` (único), `nombre` y `parroquia_id` referenciando una Parroquia existente.
3. THE Backend SHALL almacenar Recintos con los campos `codigo` (único), `nombre`, `direccion`, `nro_juntas_masculino`, `nro_juntas_femenino` y `nro_votantes`.
4. THE Backend SHALL almacenar Juntas con los campos `codigo` (único), `nombre`, `recinto_id`, `numero`, `tipo` (valor `m` o `f`), `nro_votantes` y `delegado_id` (nullable).
5. IF se intenta crear o actualizar una Zona con un `parroquia_id` inexistente, THEN THE Backend SHALL retornar un error HTTP 422 con un mensaje descriptivo.
6. IF se intenta crear o actualizar una Junta con un `recinto_id` inexistente, THEN THE Backend SHALL retornar un error HTTP 422 con un mensaje descriptivo.

---

### Requisito 2: Importación de datos desde CSV

**User Story:** Como administrador, quiero importar parroquias, zonas, recintos y juntas desde archivos CSV, para cargar masivamente la estructura electoral sin ingreso manual.

#### Criterios de Aceptación

1. WHEN el administrador envía un archivo CSV de Parroquias al endpoint de importación, THE Importador_CSV SHALL parsear cada fila y persistir los registros en la base de datos.
2. WHEN el administrador envía un archivo CSV de Zonas al endpoint de importación, THE Importador_CSV SHALL parsear cada fila y persistir los registros asociando cada Zona a su Parroquia mediante `parroquia_id`.
3. WHEN el administrador envía un archivo CSV de Recintos al endpoint de importación, THE Importador_CSV SHALL parsear cada fila y persistir los registros en la base de datos.
4. WHEN el administrador envía un archivo CSV de Juntas al endpoint de importación, THE Importador_CSV SHALL parsear cada fila y persistir los registros asociando cada Junta a su Recinto mediante `recinto_id`.
5. IF una fila del CSV contiene un campo obligatorio vacío, THEN THE Importador_CSV SHALL omitir esa fila y registrar el número de fila y el campo faltante en un reporte de errores retornado al administrador.
6. IF una fila del CSV contiene un `codigo` duplicado respecto a un registro ya existente, THEN THE Importador_CSV SHALL actualizar el registro existente con los nuevos valores (upsert).
7. WHEN la importación finaliza, THE Importador_CSV SHALL retornar un resumen con el número de registros insertados, actualizados y omitidos.
8. FOR ALL archivos CSV importados, parsear el archivo y luego serializar los registros resultantes y volver a parsearlos SHALL producir registros equivalentes (propiedad round-trip del parser CSV).

---

### Requisito 3: Totalización jerárquica de votantes

**User Story:** Como administrador, quiero que el número de votantes de las juntas se totalice automáticamente hacia arriba en la jerarquía, para tener cifras consolidadas en recintos, zonas y parroquias.

#### Criterios de Aceptación

1. WHEN se crea o actualiza el `nro_votantes` de una Junta, THE Backend SHALL recalcular el `nro_votantes` del Recinto al que pertenece como la suma de `nro_votantes` de todas sus Juntas.
2. WHEN se recalcula el `nro_votantes` de un Recinto, THE Backend SHALL recalcular el `nro_votantes` de la Zona a la que pertenece el Recinto como la suma de `nro_votantes` de todos sus Recintos.
3. WHEN se recalcula el `nro_votantes` de una Zona, THE Backend SHALL recalcular el `nro_votantes` de la Parroquia a la que pertenece la Zona como la suma de `nro_votantes` de todas sus Zonas.
4. WHEN se recalcula el `nro_juntas_masculino` de un Recinto, THE Backend SHALL calcularlo como el conteo de Juntas de tipo `m` asociadas a ese Recinto.
5. WHEN se recalcula el `nro_juntas_femenino` de un Recinto, THE Backend SHALL calcularlo como el conteo de Juntas de tipo `f` asociadas a ese Recinto.
6. FOR ALL Parroquias, la suma de `nro_votantes` de todas sus Zonas SHALL ser igual al `nro_votantes` de la Parroquia (invariante de consistencia jerárquica).

---

### Requisito 4: Gestión de candidatos y partidos

**User Story:** Como administrador, quiero registrar partidos y candidatos con su orden en la papeleta, para que los delegados puedan reportar votos por candidato.

#### Criterios de Aceptación

1. THE Backend SHALL almacenar Partidos con los campos `id`, `codigo` (único) y `nombre`.
2. THE Backend SHALL almacenar Candidatos con los campos `id`, `nombre`, `partido_id` referenciando un Partido existente y `orden_papeleta` (entero positivo único).
3. IF se intenta crear un Candidato con un `partido_id` inexistente, THEN THE Backend SHALL retornar un error HTTP 422 con un mensaje descriptivo.
4. IF se intenta crear un Candidato con un `orden_papeleta` ya asignado a otro Candidato, THEN THE Backend SHALL retornar un error HTTP 422 indicando el conflicto.

---

### Requisito 5: Gestión de delegados y asignación a juntas

**User Story:** Como administrador, quiero registrar delegados y asignarlos a una o más juntas, para que cada delegado sepa qué juntas debe reportar.

#### Criterios de Aceptación

1. THE Backend SHALL almacenar Delegados con los campos `id`, `nombre`, `cedula` (única) y `telefono`.
2. WHEN el administrador asigna un Delegado a una Junta, THE Backend SHALL actualizar el campo `delegado_id` de la Junta con el identificador del Delegado.
3. THE Backend SHALL permitir que un mismo Delegado esté asignado a múltiples Juntas simultáneamente.
4. WHEN el administrador desasigna un Delegado de una Junta, THE Backend SHALL establecer el campo `delegado_id` de la Junta en nulo.
5. IF se intenta asignar un `delegado_id` inexistente a una Junta, THEN THE Backend SHALL retornar un error HTTP 422 con un mensaje descriptivo.

---

### Requisito 6: Inicialización de votos (Encerar)

**User Story:** Como administrador, quiero encerar la tabla de votos, para inicializar todos los registros en cero antes de comenzar la recepción de resultados.

#### Criterios de Aceptación

1. WHEN el administrador ejecuta la operación Encerar, THE Backend SHALL crear o actualizar un registro de Voto con `nro_votos = 0` para cada combinación existente de Junta y Candidato.
2. WHEN la operación Encerar finaliza, THE Backend SHALL retornar el número total de registros de Voto inicializados.
3. IF la operación Encerar se ejecuta más de una vez, THE Backend SHALL sobrescribir los valores existentes con `nro_votos = 0` sin crear registros duplicados (idempotencia).
4. FOR ALL Juntas y Candidatos existentes al momento de ejecutar Encerar, el número de registros de Voto resultantes SHALL ser igual al producto del número de Juntas por el número de Candidatos.

---

### Requisito 7: Autenticación de delegados en la App Móvil

**User Story:** Como delegado, quiero iniciar sesión en la aplicación móvil con mis credenciales, para acceder únicamente a las juntas que me han sido asignadas.

#### Criterios de Aceptación

1. WHEN un Delegado envía su `cedula` y contraseña al endpoint de login, THE Backend SHALL validar las credenciales y retornar un token de acceso JWT.
2. IF las credenciales enviadas son incorrectas, THEN THE Backend SHALL retornar un error HTTP 401 con un mensaje descriptivo.
3. WHILE un Delegado tiene una sesión activa, THE App_Movil SHALL mostrar únicamente las Juntas asignadas a ese Delegado.
4. WHEN el token JWT expira, THE App_Movil SHALL redirigir al Delegado a la pantalla de login.

---

### Requisito 8: Visualización de información de juntas en la App Móvil

**User Story:** Como delegado, quiero ver la información completa de cada junta asignada, para conocer el contexto territorial y los datos del recinto antes de reportar votos.

#### Criterios de Aceptación

1. WHEN un Delegado selecciona una Junta, THE App_Movil SHALL mostrar el nombre de la Parroquia, el nombre de la Zona, el nombre y dirección del Recinto, el número de Junta y el tipo (masculino/femenino).
2. THE App_Movil SHALL mostrar el `nro_votantes` registrado para la Junta seleccionada.
3. THE App_Movil SHALL mostrar la lista de Candidatos ordenada por `orden_papeleta` con el campo `nro_votos` inicializado en cero al abrir el formulario de reporte.

---

### Requisito 9: Reporte de votos por el delegado

**User Story:** Como delegado, quiero ingresar los votos reportados por la junta para cada candidato (incluyendo nulos y blancos), para registrar los resultados del acta física.

#### Criterios de Aceptación

1. WHEN un Delegado ingresa el número de votos para un Candidato y confirma el envío, THE App_Movil SHALL enviar los valores al Backend y THE Backend SHALL actualizar el campo `nro_votos` del registro de Voto existente correspondiente a esa combinación de Junta y Candidato.
2. THE App_Movil SHALL incluir en el formulario de reporte campos separados para votos nulos y votos en blanco, además de los votos por Candidato.
3. WHEN el Delegado completa todos los campos de votos, THE App_Movil SHALL calcular y mostrar la suma total de votos ingresados comparada con el `nro_votantes` de la Junta.
4. IF la suma total de votos ingresados no coincide con el `nro_votantes` de la Junta, THEN THE App_Movil SHALL mostrar una advertencia indicando la diferencia antes de permitir el envío.
5. IF la suma total de votos ingresados coincide con el `nro_votantes` de la Junta, THEN THE App_Movil SHALL habilitar el botón de confirmación final.
6. WHEN el Delegado confirma el envío, THE Backend SHALL marcar la Junta como reportada y registrar la fecha y hora del reporte.

---

### Requisito 10: Subida de imagen del acta

**User Story:** Como delegado, quiero subir una fotografía del acta física de la junta, para dejar evidencia documental del reporte de votos.

#### Criterios de Aceptación

1. WHEN el Delegado selecciona una imagen desde su dispositivo, THE App_Movil SHALL permitir la selección de archivos en formato JPG, PNG o PDF.
2. WHEN el Delegado confirma la subida, THE App_Movil SHALL enviar la imagen al Backend y THE Backend SHALL almacenar el archivo asociado a la Junta correspondiente.
3. IF el archivo supera 10 MB, THEN THE Backend SHALL retornar un error HTTP 413 con un mensaje indicando el límite de tamaño.
4. WHEN la imagen es almacenada exitosamente, THE Backend SHALL retornar la URL de acceso al archivo.

---

### Requisito 11: Aplicación web de resultados

**User Story:** Como observador electoral, quiero ver los resultados generales y filtrados por territorio, para monitorear el avance del conteo en tiempo real.

#### Criterios de Aceptación

1. THE App_Web SHALL consumir exclusivamente endpoints REST del Backend para obtener datos de resultados.
2. THE App_Web SHALL mostrar una tabla y una gráfica con el número de votos y el porcentaje de votos por Candidato a nivel general.
3. WHEN el usuario aplica un filtro por Parroquia, THE App_Web SHALL actualizar la tabla y la gráfica mostrando únicamente los votos de las Juntas pertenecientes a esa Parroquia.
4. WHEN el usuario aplica un filtro por Zona, THE App_Web SHALL actualizar la tabla y la gráfica mostrando únicamente los votos de las Juntas pertenecientes a esa Zona.
5. WHEN el usuario aplica un filtro por Recinto, THE App_Web SHALL actualizar la tabla y la gráfica mostrando únicamente los votos de las Juntas pertenecientes a ese Recinto.
6. THE App_Web SHALL mostrar en todo momento el porcentaje de votantes con votos ingresados y el porcentaje de votantes pendientes de ingreso, calculados sobre el total de `nro_votantes` del nivel de filtro activo.
7. THE App_Web SHALL mostrar la gráfica de resultados como un gráfico de barras con el porcentaje y el número absoluto de votos por Candidato.
8. WHEN no se ha aplicado ningún filtro, THE App_Web SHALL mostrar los resultados agregados de todas las Parroquias.

---

### Requisito 12: API REST del Backend

**User Story:** Como desarrollador frontend, quiero que el Backend exponga endpoints REST bien definidos, para que tanto la App Web como la App Móvil puedan consumirlos de forma predecible.

#### Criterios de Aceptación

1. THE Backend SHALL exponer endpoints CRUD para cada entidad: Parroquias, Zonas, Recintos, Juntas, Delegados, Partidos, Candidatos y Votos.
2. THE Backend SHALL exponer un endpoint de importación CSV para cada una de las entidades: Parroquias, Zonas, Recintos y Juntas.
3. THE Backend SHALL exponer un endpoint de resultados que retorne los votos agregados por Candidato, con soporte de parámetros de filtro opcionales: `parroquia_id`, `zona_id` y `recinto_id`.
4. THE Backend SHALL exponer un endpoint de progreso que retorne el porcentaje de Juntas reportadas y el porcentaje de votantes con votos ingresados, con soporte de los mismos parámetros de filtro opcionales.
5. THE Backend SHALL retornar todas las respuestas en formato JSON con códigos HTTP estándar (200, 201, 400, 401, 404, 413, 422, 500).
6. THE Backend SHALL exponer documentación interactiva de la API en la ruta `/docs` mediante Swagger UI generado automáticamente por FastAPI.
