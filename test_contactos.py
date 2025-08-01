#!/usr/bin/env python3
"""
Pruebas unitarias básicas para las funciones de etiquetado del script contactos_pais.py
"""

import sys
import os

# Añadir el directorio actual al path para importar las funciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contactos_pais import normalize, generate_tags, TAG_RULES

def test_normalize():
    """Pruebas para la función normalize"""
    print("🧪 Probando función normalize...")
    
    # Casos de prueba
    test_cases = [
        ("Ingeniería en Energías Renovables", "ingenieria en energias renovables"),
        ("LOGÍSTICA INTERNACIONAL", "logistica internacional"),
        ("CABINAS DE EXPERIMENTACIÓN", "cabinas de experimentacion"),
        ("", ""),
        (None, ""),
        ("  Ingeniería   Industrial  ", "ingenieria industrial"),
        ("Comercio Exterior & Negocios", "comercio exterior negocios"),
        ("Psicología Organizacional", "psicologia organizacional"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for input_text, expected in test_cases:
        result = normalize(input_text)
        if result == expected:
            print(f"✅ '{input_text}' -> '{result}'")
            passed += 1
        else:
            print(f"❌ '{input_text}' -> '{result}' (esperado: '{expected}')")
    
    print(f"📊 normalize: {passed}/{total} pruebas pasaron\n")
    return passed == total

def test_generate_tags():
    """Pruebas para la función generate_tags"""
    print("🧪 Probando función generate_tags...")
    
    # Casos de prueba
    test_cases = [
        # (carreras, país, expected_tags)
        ("Ingeniería en Energías Renovables", "Honduras", "honduras, entrenador energias renovables"),
        ("Logística Internacional y Comercio Exterior", "Argentina", "argentina, logistica internacional"),
        ("Ingeniería Industrial", "Colombia", "colombia, logistica internacional, cabinas de experimentacion"),
        ("Ingeniería Industrial y Logística", "Perú", "peru, logistica internacional, cabinas de experimentacion"),
        ("Administración de Empresas", "Chile", "chile"),
        ("", "México", "mexico"),
        ("Ingeniería en Energías Renovables", "", "entrenador energias renovables"),
        ("", "", ""),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for carreras, country, expected in test_cases:
        result = generate_tags(carreras, country)
        if result == expected:
            print(f"✅ Carreras: '{carreras}' | País: '{country}' -> '{result}'")
            passed += 1
        else:
            print(f"❌ Carreras: '{carreras}' | País: '{country}' -> '{result}' (esperado: '{expected}')")
    
    print(f"📊 generate_tags: {passed}/{total} pruebas pasaron\n")
    return passed == total

def test_tag_rules():
    """Verificar que TAG_RULES está correctamente definido"""
    print("🧪 Verificando TAG_RULES...")
    
    expected_keys = ["entrenador energias renovables", "logistica internacional", "cabinas de experimentacion"]
    
    # Verificar que todas las claves existen
    for key in expected_keys:
        if key in TAG_RULES:
            print(f"✅ Clave '{key}' encontrada con {len(TAG_RULES[key])} elementos")
        else:
            print(f"❌ Clave '{key}' no encontrada")
            return False
    
    # Verificar que todas las palabras clave están en minúsculas y sin tildes
    all_keywords = []
    for keywords in TAG_RULES.values():
        all_keywords.extend(keywords)
    
    for keyword in all_keywords:
        normalized = normalize(keyword)
        if keyword == normalized:
            print(f"✅ Palabra clave '{keyword}' ya está normalizada")
        else:
            print(f"⚠️  Palabra clave '{keyword}' debería estar normalizada como '{normalized}'")
    
    print("📊 TAG_RULES verificado\n")
    return True

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas unitarias para contactos_pais.py\n")
    
    tests = [
        test_normalize,
        test_generate_tags,
        test_tag_rules,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"🎯 Resumen: {passed}/{total} suites de pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        return 0
    else:
        print("💥 Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 