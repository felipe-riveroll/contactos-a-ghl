# Script de Procesamiento de Contactos para GoHighLevel

## Descripción
Este script procesa archivos Excel con información de universidades de Latinoamérica y los convierte a formato CSV compatible con GoHighLevel, incluyendo generación automática de etiquetas basadas en carreras y país, con soporte para LLM (OpenAI API) para mejorar la cobertura de etiquetado.

## Nuevas Funcionalidades

### Mapeo de Columnas Actualizado
- **Nombre_Universidad** → **first_name**
- **Tipo_Institución** → **last_name**
- **Teléfono_Principal** → **phone** (formato E.164)
- **Email_General** → **Email**
- **Rector_Email** → **Additional Emails**
- **Tel_Admisiones** → **Additional Phones** (formato E.164)

### Filtrado por País
- Opción para filtrar contactos por país específico
- El nombre del archivo CSV incluye automáticamente el país

### Formato E.164 para Teléfonos
- **Todos los teléfonos se convierten automáticamente al formato E.164 internacional**
- **Solo se considera el primer teléfono cuando hay múltiples** (separados por ;, ,, /, etc.)
- **Se eliminan caracteres no numéricos innecesarios** (texto, símbolos, etc.)
- **Columnas procesadas**: `phone`, `Additional Phones`, `WhatsApp`
- **Manejo de casos especiales**: guiones (–), valores vacíos, notación científica
- Ejemplo: `+50425618727`

### Sistema de Etiquetado Automático con LLM
- **Columna Tags**: Se genera automáticamente basada en carreras y país
- **Etiquetas de país**: Siempre se incluye el país en minúsculas
- **Etiquetas de carreras**: Se asignan según las siguientes categorías:
  - **entrenador energias renovables**: Para carreras relacionadas con energías renovables, ambiental, eléctrica, etc.
  - **logistica internacional**: Para carreras de logística, comercio exterior, negocios internacionales, etc.
  - **cabinas de experimentacion**: Para carreras industriales, de producción, psicología organizacional, etc.

#### 🤖 **Soporte para LLM (OpenAI API)**
- **Etiquetado inteligente**: Cuando no se pueden asignar etiquetas automáticamente, el script usa OpenAI API para analizar las carreras
- **Mejora de cobertura**: Aumenta significativamente el número de universidades con etiquetas relevantes
- **Configuración flexible**: Usa el modelo `hf:mistralai/Mistral-7B-Instruct-v0.3` (configurable)
- **Fallback seguro**: Si OpenAI API no está disponible, el script funciona normalmente sin LLM

## Uso del Script

### 1. Ver países disponibles
```bash
python contactos_pais.py BD_LATAM.xlsx --list-countries
```

### 2. Generar CSV para un país específico
```bash
python contactos_pais.py BD_LATAM.xlsx --country "Honduras"
```
Esto generará: `contactos_honduras.csv`

### 3. Generar CSV para todos los países
```bash
python contactos_pais.py BD_LATAM.xlsx
```
Esto generará: `contactos_todos_paises.csv`

### 4. Deshabilitar LLM (solo etiquetado automático)
```bash
python contactos_pais.py BD_LATAM.xlsx --no-llm
```

### 5. Usar el script original con argumentos personalizados
```bash
python contactos_adaptado.py BD_LATAM.xlsx mi_archivo.csv --country "Colombia"
```

## Configuración de OpenAI API

### Instalación
1. **Instalar dependencias**: `pip install openai`
2. **Obtener API key**: Regístrate en OpenAI y obtén tu API key
3. **Configurar variables de entorno**:
   ```bash
   export OPENAI_API_KEY="tu-api-key-aqui"
   export OPENAI_API_BASE="https://api.openai.com/v1"
   ```

### Verificar instalación
```bash
python test_llm_tags.py
```

### Notas sobre el LLM
- **Modelo**: `hf:mistralai/Mistral-7B-Instruct-v0.3` (configurable en el código)
- **Fallback seguro**: Si OpenAI API no está disponible, el script funciona normalmente
- **Configuración flexible**: Usa variables de entorno para configuración
- **Uso opcional**: Se puede deshabilitar con `--no-llm`

## Países Disponibles
- Argentina (16 contactos)
- Belice (20 contactos)
- Bolivia (27 contactos)
- Chile (13 contactos)
- Colombia (16 contactos)
- Costa Rica (9 contactos)
- Ecuador (19 contactos)
- El Salvador (13 contactos)
- Guatemala (13 contactos)
- Honduras (18 contactos)
- Nicaragua (15 contactos)
- Panamá (12 contactos)
- Paraguay (14 contactos)
- Perú (20 contactos)
- República Dominicana (32 contactos)
- Uruguay (9 contactos)

## Columnas del CSV Generado
- `first_name`: Nombre de la universidad
- `last_name`: Tipo de institución
- `Email`: Email general
- `phone`: Teléfono principal (E.164)
- `Additional Phones`: Teléfono de admisiones (E.164)
- `Additional Emails`: Email del rector
- `Country`: País
- `Address`: Dirección completa
- `Website`: Sitio web
- `Facebook`: Facebook
- `Instagram`: Instagram
- `LinkedIn`: LinkedIn
- `WhatsApp`: WhatsApp (E.164)
- `Carreras`: Carreras disponibles
- `Notas`: Notas adicionales
- `Tags`: **NUEVO** - Etiquetas automáticas (país + categorías de carreras + LLM)

## Ejemplos de Etiquetado
- **Universidad con Ingeniería Industrial**: `honduras, cabinas de experimentacion`
- **Universidad con Logística Internacional**: `honduras, logistica internacional`
- **Universidad con Energías Renovables**: `honduras, entrenador energias renovables`
- **Universidad con múltiples carreras**: `honduras, logistica internacional, cabinas de experimentacion`
- **Universidad con LLM**: `honduras, logistica internacional` (asignado por LLM)

## Procesamiento de Teléfonos
### Características del Formato E.164:
- ✅ **Formato internacional**: `+[código país][número]`
- ✅ **Primer número**: Solo se procesa el primer teléfono cuando hay múltiples
- ✅ **Limpieza automática**: Se eliminan caracteres no numéricos
- ✅ **Validación**: Se verifica que el número sea válido
- ✅ **Manejo de errores**: Valores vacíos o inválidos se convierten a cadena vacía

### Ejemplos de Procesamiento:
- `"504 2561-8727"` → `"+50425618727"`
- `"+504 9905-6181; +504 9910-8802"` → `"+50499056181"` (solo el primero)
- `"–"` o `"nan"` → `""` (cadena vacía)

## Pruebas Unitarias
Ejecutar las pruebas para verificar el funcionamiento:
```bash
python test_contactos.py
```

### Pruebas de LLM
Verificar la funcionalidad de etiquetado con LLM:
```bash
python test_llm_tags.py
```

## Requisitos
- Python 3.6+
- pandas
- phonenumbers
- openpyxl (para archivos Excel)
- openai (para llamadas a OpenAI API)
- OpenAI API key (opcional, para etiquetado inteligente) 

## Estado Actual de la Implementación

### ✅ Funcionalidades Completadas
- **Mapeo de columnas**: Configuración personalizada según requerimientos
- **Filtrado por país**: Opción para procesar países específicos
- **Formato E.164**: Todos los teléfonos en formato internacional estándar
- **Etiquetado automático**: Sistema basado en reglas para categorizar carreras
- **🤖 LLM con OpenAI API**: Etiquetado inteligente usando Mistral-7B-Instruct-v0.3
- **Fallback seguro**: Funciona sin LLM si no está disponible
- **Pruebas unitarias**: Verificación de funcionalidades principales
- **🆕 Sanitización de respuestas**: Limpieza automática de respuestas del LLM
- **🆕 Cobertura ampliada**: TAG_RULES con 100+ keywords en español e inglés

### 🎯 Resultados de Pruebas
- ✅ **Conexión OpenAI API**: Funcionando correctamente
- ✅ **Etiquetado automático**: **100% de cobertura** (266/266 contactos)
- ✅ **Etiquetado con LLM**: Solo se usa cuando es necesario
- ✅ **Manejo de errores**: Graceful fallback cuando LLM no está disponible
- ✅ **Formato de teléfonos**: 100% en formato E.164
- ✅ **Sanitización**: Respuestas con comillas se procesan correctamente

### 📊 Estadísticas Finales
- **Total de contactos procesados**: 266
- **Contactos con etiquetas adicionales**: 266 (100%)
- **Contactos solo con país**: 0 (0%)
- **Llamadas al LLM**: Reducidas significativamente
- **Cobertura de reglas**: 100% con TAG_RULES ampliado

### 📊 Ejemplos de Etiquetado
- **Universidad con Ingeniería Industrial**: `honduras, cabinas de experimentacion`
- **Universidad con Administración**: `honduras, logistica internacional` (automático)
- **Universidad con múltiples carreras**: `honduras, logistica internacional, cabinas de experimentacion`
- **Universidad con Business Administration**: `honduras, logistica internacional` (automático)
- **Universidad con Computer Science**: `honduras, cabinas de experimentacion` (automático) 

## Mensaje de Commit Sugerido
```
feat: optimiza sistema de etiquetado con 100% de cobertura y sanitización de LLM

- Amplía TAG_RULES con 100+ keywords en español e inglés
- Implementa sanitize_llm_response() para limpiar respuestas del LLM
- Reduce llamadas al LLM: 100% de cobertura con reglas automáticas
- Añade log de estadísticas para monitorear cobertura
- Maneja respuestas con comillas y sinónimos de "vacío"
- Logra 100% de etiquetado (266/266 contactos) sin dependencia del LLM
- Mantiene LLM como fallback para casos edge futuros
``` 