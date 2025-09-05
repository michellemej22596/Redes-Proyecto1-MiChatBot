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

def create_summary(text):
    # Usamos OpenAI para crear un resumen del texto
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=f"Please summarize the following text:\n{text}",
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def generate_flashcards(text):
    # Aquí generamos flashcards a partir del texto
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=f"Generate flashcards from the following text:\n{text}",
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
