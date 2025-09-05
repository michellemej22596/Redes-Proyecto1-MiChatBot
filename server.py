import openai
from dotenv import load_dotenv
import os
import logging

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la clave de la API desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configurar el logging
logging.basicConfig(
    filename="chatbot_interactions.log",  # Guardar los logs en un archivo
    level=logging.INFO,  # Nivel de los mensajes a registrar (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
)

# Historial de la conversación para mantener el contexto
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def ask_llm(question):
    try:
        # Añadir la nueva pregunta del usuario al historial
        conversation_history.append({"role": "user", "content": question})

        # Loggear la solicitud
        logging.info(f"User Question: {question}")

        # Realizar la consulta al modelo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # O puedes usar "gpt-4"
            messages=conversation_history
        )

        # Obtener la respuesta generada por el modelo
        assistant_reply = response['choices'][0]['message']['content'].strip()

        # Añadir la respuesta del asistente al historial para futuras interacciones
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        # Loggear la respuesta
        logging.info(f"Assistant Response: {assistant_reply}")

        return assistant_reply

    except Exception as e:
        # En caso de error, loggear el error
        logging.error(f"Error: {str(e)}")
        return f"Error: {str(e)}"

# Ejemplo de uso
question1 = "Who was Alan Turing?"
answer1 = ask_llm(question1)
print("Answer to Q1:", answer1)

question2 = "When was he born?"
answer2 = ask_llm(question2)
print("Answer to Q2:", answer2)
