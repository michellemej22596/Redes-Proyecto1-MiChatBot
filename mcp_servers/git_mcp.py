import requests
import os
import logging
from datetime import datetime
import base64

# Leer el token de acceso de GitHub desde el archivo .env
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_github_repo(repo_name, description="", private=False):
    """ Crea un repositorio en GitHub con manejo mejorado de errores """
    try:
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        data = {
            "name": repo_name,
            "description": description or f"Repositorio creado por Genius Notes MCP - {datetime.now().strftime('%Y-%m-%d')}",
            "private": private,
            "auto_init": True
        }

        logger.info(f"Creating GitHub repository: {repo_name}")
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

def create_readme(content, title="Project README"):
    """ Crea el contenido del archivo README.md con formato mejorado """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"""# {title}

{content}

---
*Generado automáticamente por Genius Notes MCP el {timestamp}*
"""

def commit_file_to_repo(owner, repo_name, file_path, content, commit_message):
    """ Realiza commit de un archivo específico al repositorio """
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
        
        logger.info(f"Committing file {file_path} to {owner}/{repo_name}")
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

def commit_to_github(repo_name, readme_content, title="Project README"):
    """ Realiza un commit y sube el archivo README al repositorio de GitHub """
    try:
        # Crear repositorio
        repo = create_github_repo(repo_name)
        owner = repo["owner"]["login"]
        repo_url = repo["html_url"]

        # Crear contenido del README
        readme = create_readme(readme_content, title)

        # Hacer commit del README
        commit_file_to_repo(
            owner, 
            repo_name, 
            "README.md", 
            readme, 
            "Initial commit: Add README with generated content"
        )

        logger.info(f"Repository setup completed: {repo_url}")
        return {
            "repo_url": repo_url,
            "owner": owner,
            "name": repo_name,
            "created_at": repo["created_at"]
        }
    except Exception as e:
        logger.error(f"Error in commit_to_github: {str(e)}")
        raise

def create_study_repository(repo_name, study_content):
    """ Crea un repositorio completo con material de estudio organizado """
    try:
        # Crear repositorio base
        repo_info = commit_to_github(
            repo_name, 
            study_content.get('summary', 'Material de estudio generado por Genius Notes MCP'),
            f"Material de Estudio: {repo_name}"
        )
        
        owner = repo_info['owner']
        
        # Agregar flashcards como archivo separado si están disponibles
        if 'flashcards' in study_content:
            flashcards_content = f"""# Flashcards - {repo_name}

{study_content['flashcards']}

## Instrucciones de Uso

1. Lee cada pregunta cuidadosamente
2. Intenta responder mentalmente antes de ver la respuesta
3. Revisa las flashcards regularmente para mejor retención

---
*Generado por Genius Notes MCP*
"""
            commit_file_to_repo(
                owner,
                repo_name,
                "flashcards.md",
                flashcards_content,
                "Add flashcards for study"
            )
        
        # Agregar notas de estudio si están disponibles
        if 'study_notes' in study_content:
            notes_content = f"""# Notas de Estudio - {repo_name}

{study_content['study_notes']}

---
*Generado por Genius Notes MCP*
"""
            commit_file_to_repo(
                owner,
                repo_name,
                "study_notes.md",
                notes_content,
                "Add detailed study notes"
            )
        
        logger.info(f"Study repository created successfully: {repo_info['repo_url']}")
        return repo_info
        
    except Exception as e:
        logger.error(f"Error creating study repository: {str(e)}")
        raise
