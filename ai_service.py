import os 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") )

def create_simple_task(description):
    if not client.api_key:
        return ["Error: OpenAI API isn't configurated"]

    try:
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accionables
Tarea: {description}
Formato de respuesta:
- Subtarea 1
- Subtarea 2
- Subtarea 3
- etc.
Response solo con la lista de subtareas, una por línea, enpoezado cada línea con un guion."""
        params = {
            "model": "gpt-5",
            "messages": [
                {"role": "system", "content": "Eres un asistente experto en gestion de tareas que ayuda a dividir tareas complejas en pases simples y accionables"},
                {"role": "user", "content": prompt}
            ],
            "max_completion_tokens": 300,
            "verbosity": "medium",
            "reasoning_effort": "minimal"
        }

        response = client.chat.completions.create(**params)
        content = response.choices[0].message.content.strip()

        subtasks = []

        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)

        return subtasks if subtasks else ["Error: Not found any task"]
    except Exception:
        return ["Error: It's not possible to connect to OpenAI"]
    