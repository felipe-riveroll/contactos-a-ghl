#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de etiquetado con LLM usando OpenAI API
"""

import sys
import os

# Añadir el directorio actual al path para importar las funciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contactos_pais import query_openai_for_tags, generate_tags

def test_llm_functionality():
    """Probar la funcionalidad del LLM con casos de ejemplo"""
    print("🧪 Probando funcionalidad de etiquetado con LLM...")
    print("=" * 60)
    
    # Casos de prueba
    test_cases = [
        {
            "carreras": "Administración de Empresas, Gerencia de Empresas (Emprendimiento)",
            "pais": "Honduras",
            "expected": "logistica internacional"
        },
        {
            "carreras": "Medicina, Enfermería, Odontología",
            "pais": "Argentina",
            "expected": "ninguna"  # No debería asignar ninguna etiqueta
        },
        {
            "carreras": "Ingeniería en Sistemas, Informática, Tecnología de la Información",
            "pais": "Colombia",
            "expected": "cabinas de experimentacion"
        },
        {
            "carreras": "Administración de Empresas, Contabilidad, Finanzas",
            "pais": "Perú",
            "expected": "logistica internacional"
        }
    ]
    
    print("📋 Casos de prueba:")
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. Carreras: {case['carreras']}")
        print(f"   País: {case['pais']}")
        print(f"   Esperado: {case['expected']}")
        print()
    
    print("🚀 Iniciando pruebas...")
    print("-" * 60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"Prueba {i}:")
        print(f"Carreras: {case['carreras']}")
        print(f"País: {case['pais']}")
        
        # Probar la función del LLM directamente
        llm_result = query_openai_for_tags(case['carreras'], case['pais'])
        print(f"Resultado LLM: '{llm_result}'")
        
        # Probar la función completa de generación de tags
        full_result = generate_tags(case['carreras'], case['pais'])
        print(f"Resultado completo: '{full_result}'")
        
        if llm_result:
            print(f"✅ LLM asignó etiqueta: {llm_result}")
        else:
            print(f"❌ LLM no pudo asignar etiqueta")
        
        print("-" * 60)

def test_openai_connection():
    """Probar la conexión con OpenAI API"""
    print("🔌 Probando conexión con OpenAI API...")
    
    try:
        import openai
        
        # Verificar variables de entorno
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_API_BASE")
        
        if not api_key:
            print("❌ OPENAI_API_KEY no está configurada")
            print("💡 Configura la variable de entorno: export OPENAI_API_KEY='tu-api-key'")
            return False
        
        if not base_url:
            print("❌ OPENAI_API_BASE no está configurada")
            print("💡 Configura la variable de entorno: export OPENAI_API_BASE='https://api.openai.com/v1'")
            return False
        
        # Crear cliente de prueba
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        
        # Probar conexión con una petición simple
        completion = client.chat.completions.create(
            model="hf:mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
                {"role": "user", "content": "Responde solo con 'OK'"}
            ],
            max_tokens=10,
            temperature=0
        )
        
        response = completion.choices[0].message.content.strip()
        if response:
            print(f"✅ Conexión exitosa con OpenAI API")
            print(f"📦 Modelo: hf:mistralai/Mistral-7B-Instruct-v0.3")
            return True
        else:
            print(f"❌ Respuesta vacía de la API")
            return False
            
    except openai.AuthenticationError:
        print("❌ Error de autenticación con OpenAI API")
        print("💡 Verifica que tu API key sea correcta")
        return False
    except openai.APIError as e:
        print(f"❌ Error en petición a OpenAI API: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🤖 Pruebas de Etiquetado con LLM (OpenAI API)")
    print("=" * 60)
    
    # Verificar conexión con OpenAI API
    if not test_openai_connection():
        print("\n⚠️  No se puede conectar a OpenAI API. Las pruebas de LLM fallarán.")
        print("💡 Para configurar OpenAI API:")
        print("   1. Obtén una API key de OpenAI")
        print("   2. Configura las variables de entorno:")
        print("      export OPENAI_API_KEY='tu-api-key'")
        print("      export OPENAI_API_BASE='https://api.openai.com/v1'")
        return 1
    
    print("\n" + "=" * 60)
    
    # Probar funcionalidad
    test_llm_functionality()
    
    print("\n🎯 Pruebas completadas")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 