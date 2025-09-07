"""
Servidor MCP Mejorado - Genius Notes
-----------------------------------

Servidor MCP actualizado con las mejores prácticas:
- API moderna de OpenAI
- Manejo robusto de errores
- Logging mejorado
- Soporte para múltiples formatos
- Integración con GitHub
"""

import os
import logging
import asyncio
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from jsonrpcserver import method, dispatch
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import requests
import base64

# ==========================
# Configuración inicial
# ==========================
load_dotenv()

# Configurar clientes
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Configurar logging mejorado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("genius_notes_mcp.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask con CORS
app = Flask(__name__)
CORS(app)

# ==========================
# Funciones de procesamiento de archivos
# ==========================
def read_pdf(file_path):
    """Lee y extrae texto de archivos PDF"""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(reader.pages):
                try:
                    text += page.extract_text() + "\n"
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {str(e)}")
            return text.strip()
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {str(e)}")
        raise

def read_markdown(file_path):
    """Lee archivos Markdown"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading Markdown {file_path}: {str(e)}")
        raise

def read_text_file(file_path):
    """Lee archivos de texto plano"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {str(e)}")
        raise

def process_file(file_path):
    """Procesa archivos según su extensión"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == ".pdf":
        return read_pdf(file_path)
    elif file_ext in [".md", ".markdown"]:
        return read_markdown(file_path)
    elif file_ext in [".txt", ".text"]:
        return read_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Supported: .pdf, .md, .txt")

# ==========================
# Funciones de IA mejoradas
# ==========================
def generate_summary(text, max_length=200):
    """Genera resumen usando OpenAI API moderna"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un asistente experto en crear resúmenes concisos y útiles. Genera resúmenes claros y bien estructurados."
                },
                {
                    "role": "user", 
                    "content": f"Por favor, crea un resumen conciso del siguiente texto (máximo {max_length} palabras):\n\n{text[:4000]}"
                }
            ],
            max_tokens=max_length * 2,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise

def generate_flashcards(text, num_cards=5):
    """Genera flashcards usando OpenAI API moderna"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un experto en crear flashcards educativas. Genera preguntas y respuestas claras y útiles para el estudio."
                },
                {
                    "role": "user", 
                    "content": f"Crea {num_cards} flashcards del siguiente texto. Formato: 'P: [pregunta] | R: [respuesta]':\n\n{text[:4000]}"
                }
            ],
            max_tokens=400,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise

def generate_study_notes(text):
    """Genera notas de estudio estructuradas"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un experto en crear notas de estudio bien organizadas. Estructura la información de manera clara con puntos clave, conceptos importantes y ejemplos."
                },
                {
                    "role": "user", 
                    "content": f"Crea notas de estudio estructuradas del siguiente texto:\n\n{text[:4000]}"
                }
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating study notes: {str(e)}")
        raise

# ==========================
# Funciones de GitHub mejoradas
# ==========================
def create_github_repo(repo_name, description="", private=False):
    """Crea un repositorio en GitHub con manejo de errores mejorado"""
    try:
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "name": repo_name,
            "description": description or f"Repositorio creado por Genius Notes - {datetime.now().strftime('%Y-%m-%d')}",
            "private": private,
            "auto_init": True
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            repo_data = response.json()
            logger.info(f"Repository created successfully: {repo_data['html_url']}")
            return repo_data
        else:
            error_msg = f"Error creating repo: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    except Exception as e:
        logger.error(f"Error in create_github_repo: {str(e)}")
        raise

def commit_file_to_repo(owner, repo_name, file_path, content, commit_message):
    """Realiza commit de un archivo al repositorio"""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Codificar contenido en base64
        content_encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        data = {
            "message": commit_message,
            "content": content_encoded
        }
        
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            logger.info(f"File committed successfully: {file_path}")
            return response.json()
        else:
            error_msg = f"Error committing file: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
    except Exception as e:
        logger.error(f"Error in commit_file_to_repo: {str(e)}")
        raise

# ==========================
# Métodos MCP expuestos
# ==========================
@method
def process_document(file_path: str, options: dict = None):
    """
    Procesa un documento y genera contenido educativo
    
    Args:
        file_path: Ruta al archivo a procesar
        options: Opciones adicionales (summary_length, num_flashcards, etc.)
    
    Returns:
        dict: Resultado del procesamiento con resumen, flashcards y notas
    """
    try:
        logger.info(f"Processing document: {file_path}")
        
        # Configurar opciones por defecto
        opts = options or {}
        summary_length = opts.get('summary_length', 200)
        num_flashcards = opts.get('num_flashcards', 5)
        include_notes = opts.get('include_notes', True)
        
        # Procesar archivo
        text = process_file(file_path)
        
        if not text.strip():
            raise ValueError("El archivo está vacío o no se pudo extraer texto")
        
        # Generar contenido
        result = {
            "file_path": file_path,
            "file_size": len(text),
            "processed_at": datetime.now().isoformat(),
            "summary": generate_summary(text, summary_length),
            "flashcards": generate_flashcards(text, num_flashcards)
        }
        
        if include_notes:
            result["study_notes"] = generate_study_notes(text)
        
        logger.info(f"Document processed successfully: {file_path}")
        return {"success": True, "data": result}
        
    except Exception as e:
        error_msg = f"Error processing document {file_path}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

@method
def create_study_repo(repo_name: str, content: dict, options: dict = None):
    """
    Crea un repositorio de GitHub con material de estudio
    
    Args:
        repo_name: Nombre del repositorio
        content: Contenido a incluir (summary, flashcards, notes)
        options: Opciones adicionales (private, description)
    
    Returns:
        dict: Información del repositorio creado
    """
    try:
        logger.info(f"Creating study repository: {repo_name}")
        
        opts = options or {}
        description = opts.get('description', 'Repositorio de material de estudio generado por Genius Notes')
        private = opts.get('private', False)
        
        # Crear repositorio
        repo_data = create_github_repo(repo_name, description, private)
        owner = repo_data['owner']['login']
        
        # Crear README.md
        readme_content = f"""# {repo_name}

Repositorio de material de estudio generado por Genius Notes MCP

## 📋 Resumen

{content.get('summary', 'No disponible')}

## 🎯 Flashcards

{content.get('flashcards', 'No disponibles')}

## 📚 Notas de Estudio

{content.get('study_notes', 'No disponibles')}

---
*Generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Commit del README
        commit_file_to_repo(
            owner, 
            repo_name, 
            "README.md", 
            readme_content, 
            "Initial commit: Add study materials"
        )
        
        result = {
            "repo_url": repo_data['html_url'],
            "clone_url": repo_data['clone_url'],
            "created_at": repo_data['created_at'],
            "owner": owner,
            "name": repo_name
        }
        
        logger.info(f"Study repository created successfully: {result['repo_url']}")
        return {"success": True, "data": result}
        
    except Exception as e:
        error_msg = f"Error creating study repository {repo_name}: {str(e)}"
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
                "study_materials_creation"
            ],
            "supported_formats": [".pdf", ".md", ".txt"],
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
        logger.info(f"Received JSON-RPC request: {request_data[:200]}...")
        
        response = dispatch(request_data)
        
        if response:
            logger.info(f"Sending response: {str(response)[:200]}...")
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
    
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=False,
        threaded=True
    )
