# Importación de Datos - CSV

## Archivos de Ejemplo

En el directorio del backend se encuentran archivos CSV de ejemplo que puedes usar como referencia:

### `parroquias_ejemplo.csv`
Estructura para importar parroquias:
```
codigo,nombre,nro_juntas_masculino,nro_juntas_femenino,nro_votantes
001,Parroquia Centro,3,2,5000
002,Parroquia Norte,2,2,4500
```

**Columnas requeridas:**
- `codigo`: Código único de la parroquia
- `nombre`: Nombre de la parroquia
- `nro_juntas_masculino`: Número de juntas masculinas (opcional, defecto 0)
- `nro_juntas_femenino`: Número de juntas femeninas (opcional, defecto 0)
- `nro_votantes`: Número de votantes (opcional, defecto 0)

---

### `zonas_ejemplo.csv`
Estructura para importar zonas:
```
codigo,nombre,parroquia_codigo
Z001,Zona A,001
Z002,Zona B,001
```

**Columnas requeridas:**
- `codigo`: Código único de la zona
- `nombre`: Nombre de la zona
- `parroquia_codigo`: Código de la parroquia a la que pertenece (DEBE EXISTIR)

---

### `recintos_ejemplo.csv`
Estructura para importar recintos:
```
codigo,nombre,zona_codigo,direccion,nro_votantes
R001,Recinto 1,Z001,Calle 1 #123,1000
R002,Recinto 2,Z001,Calle 2 #456,1100
```

**Columnas requeridas:**
- `codigo`: Código único del recinto
- `nombre`: Nombre del recinto
- `zona_codigo`: Código de la zona (DEBE EXISTIR)
- `direccion`: Dirección (opcional)
- `nro_votantes`: Número de votantes (opcional, defecto 0)

---

### `juntas_ejemplo.csv`
Estructura para importar juntas:
```
codigo,nombre,recinto_codigo,numero,tipo,nro_votantes
J001,Junta 1,R001,001,Ordinaria,100
J002,Junta 2,R001,002,Ordinaria,110
```

**Columnas requeridas:**
- `codigo`: Código único de la junta
- `nombre`: Nombre de la junta
- `recinto_codigo`: Código del recinto (DEBE EXISTIR)
- `numero`: Número de junta
- `tipo`: Tipo de junta (ej: "Ordinaria", "Mesa de votación")
- `nro_votantes`: Número de votantes (opcional, defecto 0)

---

## Orden de Importación

1. **Primero:** Importar Parroquias
2. **Segundo:** Importar Zonas (requieren parroquias existentes)
3. **Tercero:** Importar Recintos (requieren zonas existentes)
4. **Cuarto:** Importar Juntas (requieren recintos existentes)

---

## Cómo Usar

1. Ve a **Administrativo > Gestión de Territorios**
2. Selecciona la pestaña correspondiente (Parroquias, Zonas, Recintos, Juntas)
3. Haz clic en "Seleccionar archivo" y elige el CSV
4. Haz clic en "Importar CSV"
5. Verás un resumen con:
   - ✓ Registros insertados
   - ✓ Registros actualizados
   - ⚠️ Errores (si los hay)

---

## Notas

- Los archivos DEBEN estar en formato CSV (separado por comas)
- La **primera fila debe contener los nombres de las columnas**
- Los códigos deben ser **únicos** por tabla
- Si importas un código que ya existe, se **actualizará**
- Los campos opcionales pueden dejarse en blanco o no incluirse
- Solo los **administradores** pueden importar datos

---

## Archivos Disponibles

Los archivos de ejemplo están ubicados en:
```
c:\eleciones\eleciones\control-electoral\backend\
  - parroquias_ejemplo.csv
  - zonas_ejemplo.csv
  - recintos_ejemplo.csv
  - juntas_ejemplo.csv
```

Puedes copiarlos y modificarlos según tus necesidades.
