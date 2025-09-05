# git_mcp.py
import requests
import os

# Leer el token de acceso de GitHub desde el archivo .env
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def create_github_repo(repo_name):
    """ Crea un repositorio en GitHub """
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": repo_name,
        "description": "Generated repo from Genius Notes Chatbot",
        "private": False
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error creating repo: {response.status_code} - {response.text}")

def create_readme(content):
    """ Crea el contenido del archivo README.md """
    return f"# Project README\n\n{content}"

def commit_to_github(repo_name, readme_content):
    """ Realiza un commit y sube el archivo README al repositorio de GitHub """
    repo = create_github_repo(repo_name)
    repo_url = repo["html_url"]

    readme = create_readme(readme_content)

    commit_data = {
        "message": "Initial commit with README",
        "content": readme.encode("utf-8").decode("utf-8"),
        "branch": "main"
    }

    url = f"https://api.github.com/repos/{repo_name}/contents/README.md"
    response = requests.put(url, json=commit_data, headers={"Authorization": f"token {GITHUB_TOKEN}"})

    if response.status_code == 201:
        return f"Repository created successfully: {repo_url}"
    else:
        raise Exception(f"Error committing to GitHub: {response.status_code} - {response.text}")
