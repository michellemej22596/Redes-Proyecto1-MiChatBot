import openai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener la clave de la API desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Historial de mensajes para mantener el contexto
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def ask_llm(question):
    try:
        # Añadir la nueva pregunta del usuario al historial
        conversation_history.append({"role": "user", "content": question})

        # Realizar la consulta al modelo con el historial completo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        # Obtener la respuesta generada por el modelo
        assistant_reply = response['choices'][0]['message']['content'].strip()

        # Añadir la respuesta del asistente al historial para futuras interacciones
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    except Exception as e:
        return f"Error: {str(e)}"

# Ejemplo de uso
question1 = "Who was Alan Turing?"
answer1 = ask_llm(question1)
print("Answer to Q1:", answer1)

question2 = "When was he born?"
answer2 = ask_llm(question2)
print("Answer to Q2:", answer2)
