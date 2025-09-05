# server.py
import openai
from dotenv import load_dotenv
import os
import logging
from mcp_servers.filesystem_mcp import process_file, create_summary, generate_flashcards, handle_file
from mcp_servers.git_mcp import commit_to_github

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Historial de conversación
conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]

# Configurar logging
logging.basicConfig(filename="chatbot_interactions.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ask_llm(question):
    """ Consulta al modelo de OpenAI y mantiene el contexto """
    conversation_history.append({"role": "user", "content": question})

    logging.info(f"User Question: {question}")

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation_history)

    assistant_reply = response['choices'][0]['message']['content'].strip()
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    logging.info(f"Assistant Response: {assistant_reply}")

    return assistant_reply

def handle_file_interaction(file_path):
    """ Procesar archivo y generar material de estudio """
    summary, flashcards = handle_file(file_path)
    return summary, flashcards

def handle_git_interaction(repo_name, readme_content):
    """ Crear repositorio en GitHub y hacer commit """
    result = commit_to_github(repo_name, readme_content)
    return result

#Ejemplo de uso
summary, flashcards = handle_file("notes/algorithms.md")
print("Summary:", summary)
print("Flashcards:", flashcards)
