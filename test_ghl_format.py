#!/usr/bin/env python3
"""
Script de prueba para verificar que el formato GHL es correcto
"""

import pandas as pd
import os

def test_ghl_format():
    """Prueba que el archivo CSV tenga el formato correcto para GHL"""
    
    # Verificar que el archivo existe
    csv_file = "contactos_todos_paises.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Archivo {csv_file} no encontrado")
        return False
    
    # Leer el CSV forzando que las columnas de teléfono sean strings
    df = pd.read_csv(csv_file, dtype={'Phone': str, 'Additional Phone Numbers': str, 'WhatsApp': str})
    
    # Verificar encabezados requeridos
    required_headers = [
        'First Name', 'Last Name', 'Email', 'Phone', 
        'Additional Phone Numbers', 'Additional Email Addresses',
        'Country', 'Address', 'Website', 'Facebook', 'Instagram', 
        'LinkedIn', 'WhatsApp', 'Carreras', 'Notas', 'Tags'
    ]
    
    missing_headers = [h for h in required_headers if h not in df.columns]
    if missing_headers:
        print(f"❌ Encabezados faltantes: {missing_headers}")
        return False
    
    print(f"✅ Todos los encabezados requeridos están presentes")
    
    # Verificar que no hay valores NaN en campos críticos
    nan_counts = df[['First Name', 'Email', 'Phone']].isna().sum()
    if nan_counts.sum() > 0:
        print(f"⚠️  Valores NaN encontrados: {nan_counts.to_dict()}")
    else:
        print("✅ No hay valores NaN en campos críticos")
    
    # Verificar que al menos una columna de identificación tiene datos
    has_identifiers = (
        (df['First Name'] != '').any() or 
        (df['Email'] != '').any() or 
        (df['Phone'] != '').any()
    )
    
    if not has_identifiers:
        print("❌ No se encontraron identificadores válidos")
        return False
    
    print("✅ Se encontraron identificadores válidos")
    
    # Verificar formato de teléfonos (deben estar en E.164 o vacíos)
    phone_pattern = r'^\+[1-9]\d{1,14}$'
    invalid_phones = []
    
    for idx, phone in enumerate(df['Phone']):
        if phone and not pd.isna(phone) and phone != '':
            import re
            if not re.match(phone_pattern, str(phone)):
                invalid_phones.append(f"Fila {idx+1}: {phone}")
    
    if invalid_phones:
        print(f"⚠️  Teléfonos con formato inválido: {invalid_phones[:5]}...")
    else:
        print("✅ Todos los teléfonos tienen formato E.164 válido")
    
    # Verificar países válidos
    from contactos_pais import GHL_VALID_COUNTRIES
    invalid_countries = []
    
    for idx, country in enumerate(df['Country']):
        if country and not pd.isna(country) and country != '':
            if country not in GHL_VALID_COUNTRIES:
                invalid_countries.append(f"Fila {idx+1}: {country}")
    
    if invalid_countries:
        print(f"⚠️  Países no válidos: {invalid_countries[:5]}...")
    else:
        print("✅ Todos los países son válidos para GHL")
    
    print(f"\n📊 Resumen:")
    print(f"   Total de filas: {len(df)}")
    print(f"   Filas con First Name: {(df['First Name'] != '').sum()}")
    print(f"   Filas con Email: {(df['Email'] != '').sum()}")
    print(f"   Filas con Phone: {(df['Phone'] != '').sum()}")
    print(f"   Filas con Tags: {(df['Tags'] != '').sum()}")
    
    return True

if __name__ == "__main__":
    test_ghl_format() 