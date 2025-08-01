import pandas as pd
import phonenumbers
from phonenumbers import NumberParseException

def format_phone_us(num: str, default_country='US'):
    try:
        pn = phonenumbers.parse(num, default_country)
        if not phonenumbers.is_valid_number(pn):
            return None
        # E.164
        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return None

def process_excel_to_ghl_csv(input_excel, output_csv):
    df = pd.read_excel(input_excel, sheet_name=0, dtype=str)
    # Asegurar una sola hoja y tipos string
    # Normalizar nombres de columnas si fuera necesario
    # Columnas esperadas: First Name, Last Name, Email, Phone, etc.
    required = ['First Name', 'Last Name', 'Email', 'Phone']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Falta columna obligatoria: {col}")

    # Procesar teléfonos
    def clean_phone(x):
        if pd.isna(x):
            return ''
        clean = str(x).strip()
        formatted = format_phone_us(clean)
        if formatted:
            return formatted
        # intento US estándar sin country:
        try:
            pn = phonenumbers.parse(clean, 'US')
            if phonenumbers.is_valid_number(pn):
                return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.NATIONAL)
        except:
            pass
        return clean  # fallback sin formato

    df['Phone'] = df['Phone'].apply(clean_phone)

    # Si hay una columna adicional de teléfono
    if 'Additional Phone' in df.columns:
        df['Additional Phone'] = df['Additional Phone'].apply(clean_phone)

    # Exportar a CSV sin índice, codificación UTF-8
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"CSV generado: {output_csv}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Convert Excel contactos a CSV formato GoHighLevel")
    parser.add_argument('input_excel', help='Archivo Excel de origen (.xlsx)')
    parser.add_argument('output_csv', help='Nombre del CSV de salida')
    args = parser.parse_args()
    process_excel_to_ghl_csv(args.input_excel, args.output_csv)
