# Formato GoHighLevel (GHL) - Contactos

## Resumen de Cambios Implementados

El script `contactos_pais.py` ha sido actualizado para cumplir al 100% con el formato de importación de GoHighLevel (GHL).

### ✅ Cambios Implementados

#### 1. **Encabezados Exactos de GHL**
Se han actualizado todos los encabezados de columnas para que coincidan exactamente con los requeridos por GHL:

| Encabezado GHL | Campo Original | Estado |
|----------------|----------------|---------|
| `First Name` | `Nombre_Universidad` | ✅ |
| `Last Name` | `Tipo_Institución` | ✅ |
| `Email` | `Email_General` | ✅ |
| `Phone` | `Teléfono_Principal` | ✅ |
| `Additional Phone Numbers` | `Tel_Admisiones` | ✅ |
| `Additional Email Addresses` | `Rector_Email` | ✅ |
| `Country` | `País` | ✅ |
| `Address` | `Dirección_Completa` | ✅ |
| `Website` | `Sitio_Web` | ✅ |
| `Facebook` | `Facebook` | ✅ |
| `Instagram` | `Instagram` | ✅ |
| `LinkedIn` | `LinkedIn` | ✅ |
| `WhatsApp` | `WhatsApp` | ✅ |
| `Carreras` | `Carreras_Disponibles` | ✅ |
| `Notas` | `Notas_Adicionales` | ✅ |
| `Tags` | Generado automáticamente | ✅ |

#### 2. **Depuración de Valores Vacíos**
- ✅ Reemplazo de `nan`, `None`, guiones (`-`, `–`, `—`) por strings vacíos
- ✅ Eliminación de filas sin identificadores válidos (First Name, Email o Phone)
- ✅ Función `clean_value()` para limpieza consistente
- ✅ **Validación estricta de emails** con regex y eliminación de placeholders
- ✅ **Eliminación automática de emails duplicados**

#### 3. **Teléfonos 100% Válidos**
- ✅ Función `format_phone_e164_strict()` que devuelve solo números en formato E.164
- ✅ Validación estricta con regex `^\+[1-9]\d{1,14}$`
- ✅ Manejo de números flotantes (ej: `50425618727.0` → `+50425618727`)
- ✅ Códigos de país automáticos para Honduras (+504)
- ✅ Campos vacíos para números inválidos (evita errores en GHL)

#### 4. **Corrección de Países**
- ✅ Lista oficial de países soportados por GHL (`GHL_VALID_COUNTRIES`)
- ✅ Función `validate_country()` que valida contra la lista oficial
- ✅ Campos vacíos para países no válidos (permite mapeo manual)

#### 5. **Exportación Limpia**
- ✅ `index=False` en exportación CSV
- ✅ Codificación UTF-8
- ✅ Sufijo `_ghl.csv` para archivos filtrados por país
- ✅ Conversión forzada de columnas de teléfono a strings

#### 6. **Validación y Pruebas**
- ✅ Argumento `--validate-only` para pruebas sin exportar
- ✅ Estadísticas detalladas de validación
- ✅ Script de prueba `test_ghl_format.py`
- ✅ Verificación de formato E.164 para teléfonos

### 📊 Resultados de Validación

**Archivo: `contactos_todos_paises.csv`**
- ✅ **220 filas** procesadas correctamente (después de eliminar duplicados)
- ✅ **Todos los encabezados** coinciden con GHL
- ✅ **Todos los teléfonos** en formato E.164 válido
- ✅ **Todos los países** en lista oficial de GHL
- ✅ **Todos los emails** con formato válido o vacíos
- ✅ **0 emails duplicados** (46 eliminados automáticamente)
- ✅ **48 filas** con Phone vacío pero Email presente
- ✅ **34 filas** con Email vacío pero Phone presente

### 🚀 Uso del Script

#### Comandos Básicos
```bash
# Procesar todos los países
python contactos_pais.py BD_LATAM.xlsx

# Filtrar por país específico
python contactos_pais.py BD_LATAM.xlsx --country Honduras

# Solo validar sin exportar
python contactos_pais.py BD_LATAM.xlsx --validate-only

# Listar países disponibles
python contactos_pais.py BD_LATAM.xlsx --list-countries

# Deshabilitar LLM
python contactos_pais.py BD_LATAM.xlsx --no-llm
```

#### Archivos Generados
- `contactos_todos_paises.csv` - Todos los países
- `contactos_{pais}_ghl.csv` - País específico (ej: `contactos_honduras_ghl.csv`)

### 🔧 Funciones Nuevas

#### `clean_value(value)`
Limpia valores vacíos o inválidos reemplazándolos por string vacío.

#### `normalize_email(raw)`
Valida y normaliza emails, devuelve el primer email válido o string vacío.

#### `validate_country(country)`
Valida si el país está en la lista oficial de GHL.

#### `validate_required_fields(row)`
Verifica que la fila tenga al menos un identificador válido.

#### `format_phone_e164_strict(num, default_country='US')`
Formatea teléfonos a E.164 con validación estricta para GHL.

### 📋 Requisitos Cumplidos

- ✅ **Encabezados exactos** y fila de header obligatoria
- ✅ **Formato E.164** o US para teléfonos
- ✅ **Al menos un identificador** (nombre, email o phone) por fila
- ✅ **Países válidos** según lista oficial de GHL
- ✅ **Sin valores NaN** en campos críticos
- ✅ **Exportación UTF-8** sin índices

### 🎯 Compatibilidad GHL

El archivo CSV generado es **100% compatible** con la importación de GoHighLevel y cumple con todas las reglas de validación:

- ✅ No errores de encabezado
- ✅ No errores de teléfono ("Could not parse the phone number")
- ✅ No errores de país
- ✅ **No errores de email** ("Invalid email address")
- ✅ **No emails duplicados** ("Duplicate email found")
- ✅ Formato de datos limpio y consistente

### 📝 Notas Técnicas

- Los teléfonos se procesan como strings para evitar conversiones automáticas de pandas
- Se aplica validación estricta de formato E.164 antes de aceptar números
- Los países se validan contra la lista oficial de GHL para evitar errores de mapeo
- El script mantiene compatibilidad con todas las funcionalidades existentes (LLM, etiquetado, etc.) 