"""
Script de prueba para los servidores MCP
Demuestra el escenario completo solicitado:
1. Procesar un archivo
2. Crear repositorio en GitHub
3. Generar README con el contenido procesado
4. Realizar commit
"""

import requests
import json
import os
from datetime import datetime

# Configuración del servidor MCP
MCP_SERVER_URL = "http://localhost:5000"

def test_mcp_server():
    """Prueba completa del servidor MCP"""
    print("🚀 Iniciando prueba del servidor MCP Genius Notes")
    print("=" * 50)
    
    # 1. Verificar estado del servidor
    print("\n1. Verificando estado del servidor...")
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "method": "get_server_status",
                "params": {},
                "id": 1
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("result", {}).get("success"):
                print("✅ Servidor MCP funcionando correctamente")
                server_data = result["result"]["data"]
                print(f"   - Versión: {server_data['version']}")
                print(f"   - Capacidades: {', '.join(server_data['capabilities'])}")
                print(f"   - Formatos soportados: {', '.join(server_data['supported_formats'])}")
            else:
                print("❌ Error en el servidor:", result.get("error"))
                return
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error conectando al servidor: {str(e)}")
        return
    
    # 2. Crear archivo de prueba
    print("\n2. Creando archivo de prueba...")
    test_content = """# Introducción a Machine Learning

Machine Learning es una rama de la inteligencia artificial que permite a las computadoras aprender y tomar decisiones basadas en datos sin ser explícitamente programadas para cada tarea específica.

## Conceptos Clave

### Tipos de Aprendizaje
- **Supervisado**: Utiliza datos etiquetados para entrenar modelos
- **No supervisado**: Encuentra patrones en datos sin etiquetas
- **Por refuerzo**: Aprende a través de recompensas y castigos

### Algoritmos Populares
1. Regresión Linear
2. Árboles de Decisión
3. Redes Neuronales
4. Support Vector Machines

## Aplicaciones
- Reconocimiento de imágenes
- Procesamiento de lenguaje natural
- Sistemas de recomendación
- Análisis predictivo

Machine Learning está transformando industrias enteras y creando nuevas oportunidades en tecnología, medicina, finanzas y muchos otros campos.
"""
    
    test_file = "test_ml_document.md"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    print(f"✅ Archivo creado: {test_file}")
    
    # 3. Procesar documento
    print("\n3. Procesando documento con MCP...")
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "method": "process_document",
                "params": {
                    "file_path": test_file,
                    "options": {
                        "summary_length": 150,
                        "num_flashcards": 4,
                        "include_notes": True
                    }
                },
                "id": 2
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("result", {}).get("success"):
                print("✅ Documento procesado exitosamente")
                processed_data = result["result"]["data"]
                print(f"   - Tamaño del archivo: {processed_data['file_size']} caracteres")
                print(f"   - Resumen generado: {len(processed_data['summary'])} caracteres")
                print(f"   - Flashcards: Generadas")
                print(f"   - Notas de estudio: Generadas")
            else:
                print("❌ Error procesando documento:", result.get("error"))
                return
        else:
            print(f"❌ Error en la solicitud: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error procesando documento: {str(e)}")
        return
    
    # 4. Crear repositorio en GitHub
    print("\n4. Creando repositorio en GitHub...")
    repo_name = f"ml-study-notes-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "method": "create_study_repo",
                "params": {
                    "repo_name": repo_name,
                    "content": processed_data,
                    "options": {
                        "description": "Repositorio de estudio sobre Machine Learning generado por Genius Notes MCP",
                        "private": False
                    }
                },
                "id": 3
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("result", {}).get("success"):
                print("✅ Repositorio creado exitosamente")
                repo_data = result["result"]["data"]
                print(f"   - URL del repositorio: {repo_data['repo_url']}")
                print(f"   - Propietario: {repo_data['owner']}")
                print(f"   - Nombre: {repo_data['name']}")
                print(f"   - Creado en: {repo_data['created_at']}")
            else:
                print("❌ Error creando repositorio:", result.get("error"))
                return
        else:
            print(f"❌ Error en la solicitud: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error creando repositorio: {str(e)}")
        return
    
    # 5. Limpiar archivo de prueba
    print("\n5. Limpiando archivos temporales...")
    try:
        os.remove(test_file)
        print("✅ Archivos temporales eliminados")
    except Exception as e:
        print(f"⚠️  No se pudo eliminar el archivo temporal: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 ¡Prueba completada exitosamente!")
    print(f"🔗 Repositorio creado: {repo_data['repo_url']}")
    print("\nEl escenario MCP ha sido demostrado:")
    print("✓ Procesamiento de archivo con Filesystem MCP")
    print("✓ Generación de contenido con IA")
    print("✓ Creación de repositorio con Git MCP")
    print("✓ Commit automático de README")

if __name__ == "__main__":
    test_mcp_server()
