import pandas as pd
import phonenumbers
from phonenumbers import NumberParseException
import os
import unicodedata
import re
import json
import openai

# Utilidades para validación de email
EMAIL_PLACEHOLDERS = {"no disponible", "n/d", "n.d.", "nd", "sin email", "correo no disponible"}
EMAIL_SEPARATORS = [';', ',', '/', '|', '\n', '\t', ' y ']

email_regex = re.compile(
    r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$",
    re.IGNORECASE
)

def normalize_email(raw: str) -> str:
    """Devuelve el primer e-mail válido o ''."""
    if pd.isna(raw) or raw is None:
        return ""
    
    txt = str(raw).strip().lower()
    
    # Manejar casos especiales
    if txt in ['nan', 'none', 'null', 'undefined'] or txt == '':
        return ""
    
    if txt in EMAIL_PLACEHOLDERS:
        return ""
    
    # tomar solo la primera entrada si vienen varios correos
    for sep in EMAIL_SEPARATORS:
        if sep in txt:
            txt = txt.split(sep)[0].strip()
            break
    
    return txt if email_regex.match(txt) else ""

# Lista oficial de países soportados por GoHighLevel
GHL_VALID_COUNTRIES = {
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", 
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", 
    "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", 
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", 
    "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", 
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", 
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", 
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", 
    "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", 
    "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", 
    "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", 
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", 
    "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", 
    "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", 
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
    "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", 
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", 
    "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", 
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", 
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", 
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", 
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", 
    "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", 
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", 
    "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", 
    "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
}

# TODO: Externalizar TAG_RULES a archivo JSON en el futuro
TAG_RULES = {
    "entrenador energias renovables": [
        # Energías renovables y ambiental
        "ingenieria en energias renovables", "ingenieria ambiental",
        "ambiente y desarrollo", "energia y sustentabilidad",
        "energias renovables y medio ambiente", "ingenieria electrica",
        "electricidad", "forestal", "agronomica", "agroforestal",
        "ingenieria en energia", "zootecnica", "agronomia",
        "energias renovables", "civil en energia",
        "gestion de la energia y ambiente",
        # Términos en inglés
        "renewable energy", "environmental engineering", "sustainable energy",
        "environmental science", "green energy", "clean energy",
        "sustainability", "environmental management", "ecological engineering",
        "agricultural engineering", "forestry", "agronomy", "zootechnics"
    ],
    "logistica internacional": [
        # Logística y comercio
        "logistica internacional", "logistica", "comercio exterior",
        "comercio internacional", "ingenieria en logistica",
        "gestion logistica", "negocios internacionales",
        "ingenieria comercial", "ingenieria en comercio exterior",
        "logistica integral", "administracion de negocios internacionales",
        "gestion y emprendimiento", "ingenieria industrial",
        "civil industrial", "maritimas y logisticas",
        "tecnico en logistica", "tecnologo en gestion logistica",
        # Administración y negocios
        "administracion de empresas", "administracion de negocios",
        "business administration", "business management", "gerencia de empresas",
        "mba", "management and business training", "business programmes",
        "business entrepreneurship", "business", "management", "administration",
        "accounting", "economics", "finance", "marketing", "sales",
        "entrepreneurship", "business training", "business education",
        "commercial engineering", "business economics", "business studies",
        "international business", "global business", "trade", "commerce",
        "supply chain", "operations", "procurement", "distribution"
    ],
    "cabinas de experimentacion": [
        # Ingeniería industrial y producción
        "ingenieria industrial", "ingenieria de metodos",
        "industrial y de sistemas", "higiene y seguridad industrial",
        "ingenieria administrativa", "produccion industrial",
        "diseno industrial", "psicologia industrial",
        "psicologia organizacional", "mecanica industrial",
        "administracion industrial", "civil industrial",
        "ingenieria de procesos", "ingenieria sanitaria",
        "supervision de produccion", "supervision de calidad",
        # Términos en inglés
        "industrial engineering", "production engineering",
        "lean manufacturing", "operations management", "quality management",
        "process engineering", "manufacturing engineering", "industrial design",
        "organizational psychology", "industrial psychology", "work psychology",
        "human resources", "hr", "quality control", "quality assurance",
        "safety engineering", "ergonomics", "industrial safety",
        "manufacturing", "production", "operations", "process improvement",
        "six sigma", "lean", "kaizen", "continuous improvement",
        # Tecnología y sistemas
        "computer science", "information technology", "it", "informatics",
        "software engineering", "systems engineering", "information systems",
        "cybersecurity", "digital technology", "technology management",
        "technical vocational", "vocational training", "technical education",
        "auto cad", "technical programmes", "cbet training",
        # Educación y salud
        "secondary education", "junior college", "education", "teaching",
        "health", "healthcare", "nursing", "medicine", "medical",
        "licenciaturas", "carreras tecnicas", "programas tecnicos",
        "programas", "programs", "agroindustria", "agroindustry", "agribusiness", "agriculture",
        "law", "derecho", "legal studies", "ciencias sociales",
        "social sciences", "political science", "ciencias politicas"
    ]
}

def sanitize_llm_response(text: str) -> str:
    """
    Sanitiza la respuesta del LLM eliminando comillas, espacios extra y normalizando.
    
    Args:
        text (str): Respuesta raw del LLM
        
    Returns:
        str: Respuesta limpia y normalizada
    """
    if not text:
        return ""
    
    # Limpiar comillas y espacios
    text = text.strip().lower().strip('\'"')
    
    # Normalizar usando la función existente
    text = normalize(text)
    
    # Mapear sinónimos que signifiquen vacío
    aliases = {
        "nada": "",
        "ninguna": "",
        "ninguno": "",
        "no aplica": "",
        "no aplicable": "",
        "sin etiqueta": "",
        "vacio": "",
        "empty": "",
        "none": "",
        "n/a": "",
        "na": ""
    }
    
    return aliases.get(text, text)

def query_openai_for_tags(carreras_text, country_name):
    """
    Usa OpenAI API con modelo de Hugging Face para asignar etiquetas basadas en las carreras disponibles.
    
    Args:
        carreras_text (str): Texto con las carreras disponibles
        country_name (str): Nombre del país
        
    Returns:
        str: Etiquetas asignadas por el LLM o cadena vacía si falla
    """
    try:
        # Verificar que las variables de entorno estén configuradas
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_API_BASE")
        
        if not api_key:
            print("  ❌ OPENAI_API_KEY no está configurada")
            return ""
        
        if not base_url:
            print("  ❌ OPENAI_API_BASE no está configurada")
            return ""
        
        # Crear cliente de OpenAI
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        
        # Preparar el prompt para el LLM
        system_prompt = """Eres un clasificador de carreras universitarias. Tu única tarea es asignar UNA SOLA etiqueta de las siguientes opciones:

ETIQUETAS VÁLIDAS (solo estas 3):
1. "entrenador energias renovables" - Para carreras relacionadas con energías renovables, ambiental, eléctrica, forestal, agronómica, etc.
2. "logistica internacional" - Para carreras de logística, comercio exterior, negocios internacionales, administración de empresas, etc.
3. "cabinas de experimentacion" - Para carreras industriales, de producción, psicología organizacional, diseño industrial, etc.

REGLAS ESTRICTAS:
- Responde SOLO con una de las 3 etiquetas exactas de arriba
- Si no hay una categoría clara, responde con una cadena vacía (nada)
- NO uses "ninguna", "ninguno", "no aplica", "ninguna de las anteriores"
- NO uses comillas en tu respuesta
- NO añadas explicaciones ni texto adicional"""

        user_prompt = f"""CARRERAS A ANALIZAR:
{carreras_text}

PAÍS: {country_name}

RESPUESTA (solo una de las 3 etiquetas o nada):"""

        # Hacer la petición a la API
        completion = client.chat.completions.create(
            model="hf:mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=20,
            temperature=0.0,
            stop=["\n", ".", "!", "?"]
        )
        
        llm_response_raw = completion.choices[0].message.content
        llm_response = sanitize_llm_response(llm_response_raw)
        
        # Si la respuesta queda vacía después de sanitizar, retornar vacío sin advertencia
        if not llm_response:
            return ""
        
        # Validar que la respuesta sea una de las etiquetas válidas
        valid_tags = list(TAG_RULES.keys())
        if llm_response in valid_tags:
            return llm_response
        else:
            print(f"  ⚠️  LLM sugirió etiqueta no válida: '{llm_response_raw}' (sanitizada: '{llm_response}')")
            return ""
            
    except openai.AuthenticationError:
        print("  ❌ Error de autenticación con OpenAI API")
        return ""
    except openai.APIError as e:
        print(f"  ❌ Error en petición a OpenAI API: {str(e)}")
        return ""
    except Exception as e:
        print(f"  ❌ Error inesperado con OpenAI API: {str(e)}")
        return ""

def normalize(text):
    """
    Normaliza el texto: convierte a minúsculas, quita tildes y devuelve string limpio.
    
    Args:
        text (str): Texto a normalizar
        
    Returns:
        str: Texto normalizado en minúsculas sin tildes
    """
    if pd.isna(text) or not text:
        return ""
    
    # Convertir a string y normalizar
    text = str(text).lower()
    
    # Quitar tildes usando unicodedata
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    
    # Limpiar caracteres especiales y espacios extra
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def clean_value(value):
    """
    Limpia valores vacíos o inválidos reemplazándolos por string vacío.
    
    Args:
        value: Valor a limpiar
        
    Returns:
        str: Valor limpio o string vacío
    """
    if pd.isna(value) or value is None:
        return ""
    
    value_str = str(value).strip()
    
    # Valores que se consideran vacíos
    empty_values = ['nan', 'none', 'null', 'undefined', '–', '-', '—', '']
    
    if value_str.lower() in empty_values or value_str == '':
        return ""
    
    return value_str

def validate_country(country):
    """
    Valida si el país está en la lista oficial de GHL.
    
    Args:
        country (str): Nombre del país a validar
        
    Returns:
        str: País válido o string vacío
    """
    if not country or pd.isna(country):
        return ""
    
    country_clean = clean_value(country)
    if not country_clean:
        return ""
    
    # Verificar si está en la lista oficial
    if country_clean in GHL_VALID_COUNTRIES:
        return country_clean
    
    # Si no está exactamente, devolver vacío para mapeo manual
    return ""

def validate_required_fields(row):
    """
    Valida que la fila tenga al menos un identificador requerido.
    
    Args:
        row: Fila del DataFrame
        
    Returns:
        bool: True si tiene al menos un identificador válido
    """
    first_name = row.get('First Name', '')
    email = row.get('Email', '')
    phone = row.get('Phone', '')
    
    # Debe tener al menos uno de los tres (ya están limpios por clean_value)
    return bool(first_name or email or phone)

def format_phone_e164_strict(num: str, default_country='US'):
    """
    Formatear teléfono al formato E.164 con validación estricta para GHL.
    Si no puede convertirse, devuelve string vacío.
    
    Args:
        num (str): Número de teléfono
        default_country (str): País por defecto para parsing
        
    Returns:
        str: Número en formato E.164 o string vacío si no es válido
    """
    if pd.isna(num) or str(num).strip() == '' or str(num).strip().lower() in ['nan', 'none']:
        return ''
    
    clean = str(num).strip()
    
    # Manejar casos especiales
    if clean in ['–', '-', '—', 'nan', 'NaN', 'None', 'none']:
        return ''
    
    # Manejar números flotantes (como 50425618727.0)
    if clean.endswith('.0'):
        clean = clean[:-2]
    
    # Manejar números en notación científica
    if 'e+' in clean.lower() or 'e-' in clean.lower():
        try:
            # Convertir de notación científica a entero
            clean = str(int(float(clean)))
        except (ValueError, OverflowError):
            return ''
    
    # Extraer solo el primer teléfono si hay múltiples
    # Buscar patrones comunes de separación
    separators = [';', ',', '/', '|', '\n', '\t', ' y ', ' - ', ' -']
    for sep in separators:
        if sep in clean:
            clean = clean.split(sep)[0].strip()
            break
    
    # Limpiar caracteres no numéricos excepto +, espacios y paréntesis
    clean = re.sub(r'[^\d\s\(\)\+\-]', '', clean)
    clean = clean.strip()
    
    # Si después de limpiar no queda nada, devolver vacío
    if not clean:
        return ''
    
    # Verificar que el número limpio tenga al menos 7 dígitos (mínimo para un teléfono)
    digits_only = re.sub(r'[^\d]', '', clean)
    if len(digits_only) < 7:
        return ''
    
    # Si el número no empieza con +, intentar agregar el código de país por defecto
    if not clean.startswith('+'):
        # Para Honduras, agregar +504
        if clean.startswith('504'):
            clean = '+' + clean
        else:
            # Intentar con el país por defecto
            clean = '+' + clean
    
    try:
        # Intentar parsear con el país por defecto
        pn = phonenumbers.parse(clean, default_country)
        if phonenumbers.is_valid_number(pn):
            formatted = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
            # Verificar que el resultado esté en formato E.164 correcto
            if re.match(r'^\+[1-9]\d{1,14}$', formatted):
                return formatted
    except NumberParseException:
        pass
    
    # Si falla, intentar sin país
    try:
        pn = phonenumbers.parse(clean)
        if phonenumbers.is_valid_number(pn):
            formatted = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
            # Verificar que el resultado esté en formato E.164 correcto
            if re.match(r'^\+[1-9]\d{1,14}$', formatted):
                return formatted
    except NumberParseException:
        pass
    
    # Si no se puede formatear a E.164, devolver vacío para evitar errores en GHL
    return ''

def generate_tags(carreras, country_name, use_llm=True):
    """
    Genera etiquetas basadas en las carreras y el país.
    
    Args:
        carreras (str): Texto con las carreras disponibles
        country_name (str): Nombre del país
        use_llm (bool): Si usar LLM para etiquetado adicional
        
    Returns:
        str: Etiquetas separadas por comas, sin duplicados
    """
    tags = []
    
    # Añadir el país como primera etiqueta
    if country_name and not pd.isna(country_name):
        country_normalized = normalize(country_name)
        if country_normalized:
            tags.append(country_normalized)
    
    # Normalizar las carreras
    carreras_normalized = normalize(carreras)
    
    if carreras_normalized:
        # Revisar cada regla de etiquetado
        for tag_name, keywords in TAG_RULES.items():
            for keyword in keywords:
                if keyword in carreras_normalized:
                    tags.append(tag_name)
                    break  # Solo añadir la etiqueta una vez por regla
    
    # Si solo tenemos la etiqueta del país y LLM está habilitado, intentar con LLM
    if use_llm and len(tags) == 1 and tags[0] == normalize(country_name):
        print(f"  🤖 Intentando asignar etiqueta con LLM para: {carreras[:50]}...")
        llm_tag = query_openai_for_tags(carreras, country_name)
        if llm_tag:
            tags.append(llm_tag)
            print(f"  ✅ LLM asignó etiqueta: {llm_tag}")
        else:
            print(f"  ❌ LLM no pudo asignar etiqueta")
    
    # Eliminar duplicados manteniendo el orden
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)
    
    return ', '.join(unique_tags)



def process_excel_to_ghl_csv(input_excel, country_filter=None, use_llm=True, validate_only=False):
    """
    Procesa Excel a CSV con formato GoHighLevel con validaciones estrictas.
    
    Args:
        input_excel (str): Ruta del archivo Excel
        country_filter (str): Filtro de país opcional
        use_llm (bool): Si usar LLM para etiquetado
        validate_only (bool): Solo validar sin exportar archivo
        
    Returns:
        str: Nombre del archivo generado o None si validate_only=True
    """
    # Leer el Excel con tipos específicos para evitar conversiones automáticas
    df = pd.read_excel(input_excel, sheet_name=0, dtype=str)
    
    # Filtrar por país si se especifica
    if country_filter:
        df = df[df['País'].str.contains(country_filter, case=False, na=False)]
        if len(df) == 0:
            print(f"No se encontraron contactos para el país: {country_filter}")
            return None
        print(f"Filtrado por país: {country_filter}")
        print(f"Contactos encontrados: {len(df)}")
    
    # Crear nuevo DataFrame con encabezados exactos de GHL
    ghl_df = pd.DataFrame()
    
    # Mapeo con encabezados exactos de GHL
    if 'Nombre_Universidad' in df.columns:
        ghl_df['First Name'] = df['Nombre_Universidad'].apply(clean_value)
    else:
        ghl_df['First Name'] = ''
    
    if 'Tipo_Institución' in df.columns:
        ghl_df['Last Name'] = df['Tipo_Institución'].apply(clean_value)
    else:
        ghl_df['Last Name'] = ''
    
    if 'Email_General' in df.columns:
        ghl_df['Email'] = df['Email_General'].apply(normalize_email)
    else:
        ghl_df['Email'] = ''
    
    # Procesar teléfonos principales con validación estricta
    if 'Teléfono_Principal' in df.columns:
        # Asegurar que se procesen como strings
        phone_series = df['Teléfono_Principal'].astype(str).replace('nan', '')
        ghl_df['Phone'] = phone_series.apply(format_phone_e164_strict)
    else:
        ghl_df['Phone'] = ''
    
    # Procesar teléfonos adicionales
    if 'Tel_Admisiones' in df.columns:
        # Asegurar que se procesen como strings
        additional_phone_series = df['Tel_Admisiones'].astype(str).replace('nan', '')
        ghl_df['Additional Phone Numbers'] = additional_phone_series.apply(format_phone_e164_strict)
    else:
        ghl_df['Additional Phone Numbers'] = ''
    
    # Procesar emails adicionales
    if 'Rector_Email' in df.columns:
        ghl_df['Additional Email Addresses'] = df['Rector_Email'].apply(normalize_email)
    else:
        ghl_df['Additional Email Addresses'] = ''
    
    # Validar países según lista oficial de GHL
    if 'País' in df.columns:
        ghl_df['Country'] = df['País'].apply(validate_country)
    else:
        ghl_df['Country'] = ''
    
    if 'Dirección_Completa' in df.columns:
        ghl_df['Address'] = df['Dirección_Completa'].apply(clean_value)
    else:
        ghl_df['Address'] = ''
    
    if 'Sitio_Web' in df.columns:
        ghl_df['Website'] = df['Sitio_Web'].apply(clean_value)
    else:
        ghl_df['Website'] = ''
    
    # Redes sociales
    if 'Facebook' in df.columns:
        ghl_df['Facebook'] = df['Facebook'].apply(clean_value)
    else:
        ghl_df['Facebook'] = ''
    
    if 'Instagram' in df.columns:
        ghl_df['Instagram'] = df['Instagram'].apply(clean_value)
    else:
        ghl_df['Instagram'] = ''
    
    if 'LinkedIn' in df.columns:
        ghl_df['LinkedIn'] = df['LinkedIn'].apply(clean_value)
    else:
        ghl_df['LinkedIn'] = ''
    
    # WhatsApp con validación estricta
    if 'WhatsApp' in df.columns:
        # Asegurar que se procesen como strings
        whatsapp_series = df['WhatsApp'].astype(str).replace('nan', '')
        ghl_df['WhatsApp'] = whatsapp_series.apply(format_phone_e164_strict)
    else:
        ghl_df['WhatsApp'] = ''
    
    # Información adicional
    if 'Carreras_Disponibles' in df.columns:
        ghl_df['Carreras'] = df['Carreras_Disponibles'].apply(clean_value)
    else:
        ghl_df['Carreras'] = ''
    
    if 'Notas_Adicionales' in df.columns:
        ghl_df['Notas'] = df['Notas_Adicionales'].apply(clean_value)
    else:
        ghl_df['Notas'] = ''
    
    # Generar columna Tags con soporte para LLM
    if use_llm:
        print("Generando etiquetas con soporte para LLM...")
    else:
        print("Generando etiquetas (LLM deshabilitado)...")
    
    ghl_df['Tags'] = ghl_df.apply(
        lambda row: generate_tags(row['Carreras'], row['Country'], use_llm=use_llm), 
        axis=1
    )

    # Filtrar filas que no cumplen con los requisitos mínimos de GHL
    initial_count = len(ghl_df)
    ghl_df = ghl_df[ghl_df.apply(validate_required_fields, axis=1)]
    filtered_count = len(ghl_df)
    
    if filtered_count < initial_count:
        print(f"⚠️  Se eliminaron {initial_count - filtered_count} filas sin identificadores válidos")

    # Log final con estadísticas de etiquetado
    total_contacts = len(ghl_df)
    
    # Contar contactos que solo tienen etiqueta de país
    def has_only_country_tag(row):
        if pd.isna(row['Tags']) or row['Tags'].strip() == '':
            return False
        country_normalized = normalize(row['Country']) if not pd.isna(row['Country']) else ""
        tags = row['Tags'].strip()
        return tags == country_normalized
    
    contacts_with_only_country = len(ghl_df[ghl_df.apply(has_only_country_tag, axis=1)])
    contacts_with_extra_tags = total_contacts - contacts_with_only_country
    
    print(f"\n📊 Estadísticas de etiquetado:")
    print(f"   Total de contactos: {total_contacts}")
    print(f"   Con etiquetas adicionales: {contacts_with_extra_tags}")
    print(f"   Solo con país: {contacts_with_only_country}")
    if contacts_with_only_country > 0:
        print(f"   ⚠️  {contacts_with_only_country} contactos quedaron solo con etiqueta de país")
        print(f"   💡 Considera añadir más keywords a TAG_RULES para mejorar cobertura")

    # Si es solo validación, mostrar estadísticas y retornar
    if validate_only:
        print(f"\n🔍 VALIDACIÓN COMPLETA:")
        print(f"   Filas finales: {total_contacts}")
        
        # Contar filas con Phone vacío pero Email presente y viceversa
        phone_empty_email_present = len(ghl_df[(ghl_df['Phone'] == '') & (ghl_df['Email'] != '')])
        email_empty_phone_present = len(ghl_df[(ghl_df['Email'] == '') & (ghl_df['Phone'] != '')])
        
        print(f"   Con Phone vacío pero Email presente: {phone_empty_email_present}")
        print(f"   Con Email vacío pero Phone presente: {email_empty_phone_present}")
        
        # Lista de países únicos que no están en la lista oficial
        unique_countries = set(ghl_df['Country'].unique())
        invalid_countries = [c for c in unique_countries if c and c not in GHL_VALID_COUNTRIES]
        
        if invalid_countries:
            print(f"   ⚠️  Países no válidos en GHL: {invalid_countries}")
        else:
            print(f"   ✅ Todos los países son válidos para GHL")
        
        return None

    # Generar nombre del archivo con el país
    if country_filter:
        # Limpiar el nombre del país para el archivo
        country_clean = country_filter.replace(' ', '_').replace('-', '_').lower()
        output_csv = f"contactos_{country_clean}_ghl.csv"
    else:
        output_csv = "contactos_todos_paises.csv"

    # Quitar duplicados de email no vacío
    initial_count = len(ghl_df)
    ghl_df = ghl_df.sort_values('Email').drop_duplicates(
        subset=['Email'], keep='first'
    )
    duplicates_removed = initial_count - len(ghl_df)
    
    # Log de limpieza de emails
    invalid_email_count = (ghl_df['Email'] == '').sum()
    print(f"❗ Emails descartados por formato/placeholder: {invalid_email_count}")
    if duplicates_removed > 0:
        print(f"❗ Emails duplicados eliminados: {duplicates_removed}")
    
    # Asegurar que las columnas de teléfono y email se guarden como strings
    phone_columns = ['Phone', 'Additional Phone Numbers', 'WhatsApp']
    for col in phone_columns:
        if col in ghl_df.columns:
            ghl_df[col] = ghl_df[col].astype(str)
    
    # Asegurar que las columnas de email se guarden como strings y reemplazar NaN
    email_columns = ['Email', 'Additional Email Addresses']
    for col in email_columns:
        if col in ghl_df.columns:
            ghl_df[col] = ghl_df[col].astype(str)
            # Reemplazar 'nan' por string vacío
            ghl_df[col] = ghl_df[col].replace('nan', '')
    
    # Exportar a CSV sin índice, codificación UTF-8
    ghl_df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"CSV generado: {output_csv}")
    print(f"Total de contactos procesados: {len(ghl_df)}")
    print(f"Columnas en el CSV: {list(ghl_df.columns)}")
    
    return output_csv

def list_available_countries(input_excel):
    """Listar todos los países disponibles en el archivo"""
    df = pd.read_excel(input_excel, sheet_name=0, dtype=str)
    countries = df['País'].unique()
    countries = [c for c in countries if pd.notna(c) and str(c).strip() != '']
    countries.sort()
    
    print("Países disponibles:")
    for i, country in enumerate(countries, 1):
        count = len(df[df['País'] == country])
        print(f"{i}. {country} ({count} contactos)")
    
    return countries

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Convert Excel contactos a CSV formato GoHighLevel con filtrado por país, generación de columna Tags y soporte para LLM")
    parser.add_argument('input_excel', help='Archivo Excel de origen (.xlsx)')
    parser.add_argument('--country', '-c', help='Filtrar por país específico (opcional)')
    parser.add_argument('--list-countries', '-l', action='store_true', help='Listar países disponibles')
    parser.add_argument('--no-llm', action='store_true', help='Deshabilitar el uso de LLM para etiquetado')
    parser.add_argument('--validate-only', action='store_true', help='Solo validar sin exportar archivo')
    args = parser.parse_args()
    
    if args.list_countries:
        list_available_countries(args.input_excel)
    else:
        # Si no se especifica país, usar todos los países
        country_filter = args.country if args.country else None
        process_excel_to_ghl_csv(args.input_excel, country_filter, use_llm=not args.no_llm, validate_only=args.validate_only) 