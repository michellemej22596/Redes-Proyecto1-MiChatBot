import openai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la clave de la API desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

def ask_llm(question):
    try:
        # Utiliza el endpoint de chat
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # modelo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content'].strip()  # Accede al texto de la respuesta

    except Exception as e:
        return f"Error: {str(e)}"

# Ejemplo de uso
question = "Eres mi asistente de estudio?"
answer = ask_llm(question)
print(answer)
