import os
import PyPDF2
import markdown
from dotenv import load_dotenv
import openai

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configurar la clave de API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Función para leer archivos PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Función para leer archivos Markdown
def read_markdown(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Función para procesar y generar resúmenes o flashcards
def process_file(file_path):
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.md'):
        return read_markdown(file_path)
    else:
        raise ValueError("Unsupported file type. Only .pdf and .md files are supported.")

# Función para crear un resumen utilizando el modelo de chat (gpt-3.5-turbo o gpt-4)
def create_summary(text):
    # Usamos el endpoint adecuado para los modelos de chat
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # O "gpt-4" si prefieres usar ese
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please summarize the following text:\n{text}"}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Función para generar flashcards utilizando el modelo de chat
def generate_flashcards(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # O "gpt-4" si prefieres usar ese
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate flashcards from the following text:\n{text}"}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()


# Función principal para manejar archivos y generar material de estudio
def handle_file(file_path):
    file_text = process_file(file_path)

    # Crear un resumen
    summary = create_summary(file_text)

    # Generar flashcards
    flashcards = generate_flashcards(file_text)

    return summary, flashcards
