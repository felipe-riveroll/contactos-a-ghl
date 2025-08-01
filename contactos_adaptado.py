import pandas as pd
import phonenumbers
from phonenumbers import NumberParseException

def format_phone_e164(num: str, default_country='US'):
    """Formatear teléfono al formato E.164"""
    if pd.isna(num) or str(num).strip() == '':
        return ''
    
    clean = str(num).strip()
    
    try:
        # Intentar parsear con el país por defecto
        pn = phonenumbers.parse(clean, default_country)
        if phonenumbers.is_valid_number(pn):
            return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        pass
    
    # Si falla, intentar sin país
    try:
        pn = phonenumbers.parse(clean)
        if phonenumbers.is_valid_number(pn):
            return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        pass
    
    # Si no se puede formatear, devolver el número original
    return clean

def process_excel_to_ghl_csv(input_excel, output_csv, country_filter=None):
    df = pd.read_excel(input_excel, sheet_name=0, dtype=str)
    
    # Filtrar por país si se especifica
    if country_filter:
        df = df[df['País'].str.contains(country_filter, case=False, na=False)]
        if len(df) == 0:
            print(f"No se encontraron contactos para el país: {country_filter}")
            return
        print(f"Filtrado por país: {country_filter}")
        print(f"Contactos encontrados: {len(df)}")
    
    # Crear nuevo DataFrame con el mapeo actualizado
    ghl_df = pd.DataFrame()
    
    # Mapeo según los nuevos requerimientos
    if 'Nombre_Universidad' in df.columns:
        ghl_df['first_name'] = df['Nombre_Universidad'].fillna('')
    else:
        ghl_df['first_name'] = ''
    
    if 'Tipo_Institución' in df.columns:
        ghl_df['last_name'] = df['Tipo_Institución'].fillna('')
    else:
        ghl_df['last_name'] = ''
    
    if 'Email_General' in df.columns:
        ghl_df['Email'] = df['Email_General'].fillna('')
    else:
        ghl_df['Email'] = ''
    
    # Procesar teléfonos principales
    if 'Teléfono_Principal' in df.columns:
        ghl_df['phone'] = df['Teléfono_Principal'].apply(format_phone_e164)
    else:
        ghl_df['phone'] = ''
    
    # Procesar teléfonos adicionales
    if 'Tel_Admisiones' in df.columns:
        ghl_df['Additional Phones'] = df['Tel_Admisiones'].apply(format_phone_e164)
    else:
        ghl_df['Additional Phones'] = ''
    
    # Procesar emails adicionales
    if 'Rector_Email' in df.columns:
        ghl_df['Additional Emails'] = df['Rector_Email'].fillna('')
    else:
        ghl_df['Additional Emails'] = ''
    
    # Agregar columnas adicionales útiles
    if 'País' in df.columns:
        ghl_df['Country'] = df['País'].fillna('')
    
    if 'Dirección_Completa' in df.columns:
        ghl_df['Address'] = df['Dirección_Completa'].fillna('')
    
    if 'Sitio_Web' in df.columns:
        ghl_df['Website'] = df['Sitio_Web'].fillna('')
    
    # Redes sociales
    if 'Facebook' in df.columns:
        ghl_df['Facebook'] = df['Facebook'].fillna('')
    
    if 'Instagram' in df.columns:
        ghl_df['Instagram'] = df['Instagram'].fillna('')
    
    if 'LinkedIn' in df.columns:
        ghl_df['LinkedIn'] = df['LinkedIn'].fillna('')
    
    if 'WhatsApp' in df.columns:
        ghl_df['WhatsApp'] = df['WhatsApp'].fillna('')
    
    # Información adicional
    if 'Carreras_Disponibles' in df.columns:
        ghl_df['Carreras'] = df['Carreras_Disponibles'].fillna('')
    
    if 'Notas_Adicionales' in df.columns:
        ghl_df['Notas'] = df['Notas_Adicionales'].fillna('')

    # Exportar a CSV sin índice, codificación UTF-8
    ghl_df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"CSV generado: {output_csv}")
    print(f"Total de contactos procesados: {len(ghl_df)}")
    print(f"Columnas en el CSV: {list(ghl_df.columns)}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Convert Excel contactos a CSV formato GoHighLevel")
    parser.add_argument('input_excel', help='Archivo Excel de origen (.xlsx)')
    parser.add_argument('output_csv', help='Nombre del CSV de salida')
    parser.add_argument('--country', '-c', help='Filtrar por país específico (opcional)')
    args = parser.parse_args()
    
    # Si no se especifica país, usar todos los países
    country_filter = args.country if args.country else None
    
    process_excel_to_ghl_csv(args.input_excel, args.output_csv, country_filter) 