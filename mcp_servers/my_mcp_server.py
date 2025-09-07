"""
Servidor MCP Local (JSON-RPC) - Genius Notes v2.0
-------------------------------------------------

Servidor MCP actualizado que integra todas las funcionalidades:
- Procesamiento de archivos (filesystem_mcp)
- Integración con GitHub (git_mcp)
- Generación de contenido con IA
- Protocolo JSON-RPC estándar
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from jsonrpcserver import method, dispatch
from dotenv import load_dotenv

from filesystem_mcp import handle_file, process_file, create_summary, generate_flashcards
from git_mcp import create_study_repository, commit_to_github, create_github_repo

# ==========================
# Configuración inicial
# ==========================
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("genius_notes_mcp.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# ==========================
# Métodos MCP expuestos vía JSON-RPC
# ==========================
@method
def process_document(file_path: str, options: dict = None):
    """
    Procesa un archivo PDF o Markdown y devuelve:
    - summary: resumen generado por el LLM
    - flashcards: flashcards generadas por el LLM
    """
    try:
        logger.info(f"Received request to process file: {file_path}")
        
        # Configurar opciones por defecto
        opts = options or {}
        
        # Procesar archivo usando el módulo filesystem_mcp
        summary, flashcards = handle_file(file_path)
        
        result = {
            "file_path": file_path,
            "processed_at": datetime.now().isoformat(),
            "summary": summary,
            "flashcards": flashcards
        }
        
        logger.info(f"Processed file successfully: {file_path}")
        return {"success": True, "data": result}
        
    except Exception as e:
        error_msg = f"Error processing file {file_path}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

@method
def create_github_repository(repo_name: str, content: dict, options: dict = None):
    """
    Crea un repositorio de GitHub con material de estudio
    """
    try:
        logger.info(f"Creating GitHub repository: {repo_name}")
        
        opts = options or {}
        
        # Usar el módulo git_mcp para crear el repositorio
        repo_info = create_study_repository(repo_name, content)
        
        logger.info(f"Repository created successfully: {repo_info['repo_url']}")
        return {"success": True, "data": repo_info}
        
    except Exception as e:
        error_msg = f"Error creating repository {repo_name}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

@method
def complete_workflow(file_path: str, repo_name: str, options: dict = None):
    """
    Flujo completo: procesa archivo y crea repositorio con el contenido
    """
    try:
        logger.info(f"Starting complete workflow: {file_path} -> {repo_name}")
        
        # 1. Procesar archivo
        process_result = process_document(file_path, options)
        if not process_result["success"]:
            return process_result
        
        processed_data = process_result["data"]
        
        # 2. Crear repositorio con el contenido procesado
        repo_content = {
            "summary": processed_data["summary"],
            "flashcards": processed_data["flashcards"]
        }
        
        repo_result = create_github_repository(repo_name, repo_content, options)
        if not repo_result["success"]:
            return repo_result
        
        # 3. Combinar resultados
        result = {
            "workflow": "complete",
            "file_processing": processed_data,
            "repository": repo_result["data"],
            "completed_at": datetime.now().isoformat()
        }
        
        logger.info(f"Complete workflow finished successfully")
        return {"success": True, "data": result}
        
    except Exception as e:
        error_msg = f"Error in complete workflow: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

@method
def get_server_status():
    """Obtiene el estado del servidor MCP"""
    try:
        status = {
            "server_name": "Genius Notes MCP",
            "version": "2.0.0",
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "capabilities": [
                "document_processing",
                "github_integration", 
                "ai_content_generation",
                "complete_workflow"
            ],
            "supported_formats": [".pdf", ".md"],
            "integrations": {
                "openai": bool(os.getenv("OPENAI_API_KEY")),
                "github": bool(os.getenv("GITHUB_TOKEN"))
            }
        }
        return {"success": True, "data": status}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==========================
# Endpoints Flask
# ==========================
@app.route("/", methods=["POST"])
def handle_jsonrpc():
    """Maneja las solicitudes JSON-RPC"""
    try:
        request_data = request.get_data().decode('utf-8')
        logger.info(f"Received JSON-RPC request")
        
        response = dispatch(request_data)
        
        if response:
            return jsonify(response)
        else:
            return jsonify({"error": "No response generated"}), 400
            
    except Exception as e:
        logger.error(f"Error handling JSON-RPC request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de verificación de salud"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "Genius Notes MCP v2.0.0"
    })

# ==========================
# Ejecución del servidor
# ==========================
if __name__ == "__main__":
    logger.info("Starting Genius Notes MCP Server v2.0.0")
    logger.info(f"OpenAI API configured: {bool(os.getenv('OPENAI_API_KEY'))}")
    logger.info(f"GitHub API configured: {bool(os.getenv('GITHUB_TOKEN'))}")
    
    print("🚀 Genius Notes MCP Server v2.0.0")
    print("=" * 40)
    print("📡 Server running on http://localhost:5000")
    print("🔧 Health check: http://localhost:5000/health")
    print("📋 Capabilities:")
    print("   • Document processing (PDF, Markdown)")
    print("   • GitHub repository creation")
    print("   • AI content generation")
    print("   • Complete workflow automation")
    print("=" * 40)
    
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=False,
        threaded=True
    )
