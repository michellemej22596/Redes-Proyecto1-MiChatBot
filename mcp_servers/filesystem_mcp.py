import os
import PyPDF2
import markdown
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Cargar las variables de entorno del archivo .env
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Función para leer archivos PDF
def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            logger.info(f"PDF processed successfully: {file_path}")
            return text
    except Exception as e:
        logger.error(f"Error reading PDF {file_path}: {str(e)}")
        raise

# Función para leer archivos Markdown
def read_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info(f"Markdown file processed successfully: {file_path}")
            return content
    except Exception as e:
        logger.error(f"Error reading Markdown {file_path}: {str(e)}")
        raise

# Función para procesar y generar resúmenes o flashcards
def process_file(file_path):
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.md'):
        return read_markdown(file_path)
    else:
        raise ValueError("Unsupported file type. Only .pdf and .md files are supported.")

def create_summary(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en crear resúmenes concisos y útiles en español."},
                {"role": "user", "content": f"Por favor, crea un resumen conciso del siguiente texto:\n{text}"}
            ],
            max_tokens=200,
            temperature=0.3
        )
        summary = response.choices[0].message.content.strip()
        logger.info("Summary generated successfully")
        return summary
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise

def generate_flashcards(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en crear flashcards educativas en español. Genera preguntas y respuestas claras."},
                {"role": "user", "content": f"Genera 5 flashcards del siguiente texto. Formato: 'P: [pregunta] | R: [respuesta]':\n{text}"}
            ],
            max_tokens=300,
            temperature=0.4
        )
        flashcards = response.choices[0].message.content.strip()
        logger.info("Flashcards generated successfully")
        return flashcards
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise

# Función principal para manejar archivos y generar material de estudio
def handle_file(file_path):
    try:
        logger.info(f"Processing file: {file_path}")
        file_text = process_file(file_path)

        # Crear un resumen
        summary = create_summary(file_text)

        # Generar flashcards
        flashcards = generate_flashcards(file_text)

        logger.info(f"File processed successfully: {file_path}")
        return summary, flashcards
    except Exception as e:
        logger.error(f"Error in handle_file: {str(e)}")
        raise
