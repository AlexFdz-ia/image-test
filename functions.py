import json
from PyPDF2 import PdfReader
import google.generativeai as genai

def check(genre, vibe, target, duration, num_characters, num_scene, num_chapters, submit, requirements, uploaded_file):
    return (genre and vibe and target and duration and num_characters and num_scene and num_chapters and submit and requirements and uploaded_file)

# Establecemos la API de Google
genai.configure(api_key="AIzaSyDJ7JahaV2HEmQx-RWPeFbvTVhYJZ8DECo")
# Seleccionamos el modelo a usar
model = genai.GenerativeModel('gemini-1.5-flash')

def read_file(file):

    # Leer el archivo PDF
    pdf_reader = PdfReader(file)
    full_text = ""

    # Extraer texto de cada página
    for page in pdf_reader.pages:
        full_text += page.extract_text()
        
    return full_text

# Funcion para generar la respuesta de Gemini
def generate_answer(chat_history, prompt):

    # Añadimos al historial el ultimo mensaje del ususario
    chat_history.append(f"User: {prompt}" + "\nAssistant:")

    # Generamos la respuesta y la añadimos al historial
    response = model.generate_content(chat_history).text
    chat_history.append(response)

    return response

def generate_characters(genre, vibe, target, num_characters):
    characters_prompt = f"""

    Crea los personajes para la historia de una novela visual interactiva. Debes tener en cuenta:

    - Género: {genre}
    - Tono de la historia: {vibe}
    - Público objetivo: {target}
    - Número de personajes: {num_characters}

    """

    characters_prompt += """

    <FORMAT>

    [
        {
            "id": "1",
            "name": "",
            "personality_traits": "",
            "visual_description": ""
        },
    ]

    </FORMAT>

    Devuelve el resultado SOLO como text, nada más.

    """

    characters = model.generate_content(characters_prompt).text

    return characters

def generate_prompt(genre, vibe, target, duration, num_scene, num_chapters, requirements, full_text, characters_dic):
    full_prompt = f"""
    Crea una historia para un videojuego estilo novela visual que puede incluir aspectos de realidad aumentada.
    Básate en la siguiente estructura. Los datos entre paréntesis () son indicadores para que tú crees el contenido basado en todo el contexto proporcionado.
    Sigue la estructrua indicada y no la cambies.
    Crea el contenido de toda la historia y de todos y cada uno de los capítulos, no generalices.
    En las pantallas dinámicas escribe siempre las preguntas con las respuetas, teniendo en cuenta el <CONTEXTO>
    Acuérdate de que debe haber diálogos.
    La duración total del videojuego debe ser de {duration} y tener {num_chapters} capítulos.
    Ten en cuenta estos requisitos:

    <REQUISITOS>
    {requirements}
    </REQUISITOS>

    <ESTRUCTURA>

    - Título: (Título de la novela)
    - Subtítulo: (Subtítulo de la novela)
    - Temática: {genre}
    - Objetivos pedagógicos: Fomentar el pensamiento crítico y la colaboración en la resolución de problemas.


    - Personajes:

    """

    characters_prompt = ""

    for character in characters_dic:
        characters_prompt += "Nombre: " + character["name"] + "Personalidad: " + character["personality_traits"] + "Descripción visual: " + character["visual_description"]

    full_prompt += characters_prompt

    full_prompt += f"""

    - Historia: (Resumen de la narrativa y el conflicto central)
    - Tipo: Serious Game
    - Género: {vibe}
    - Estructura narrativa: No lineal
    - Público objetivo: {target}
    - Lista de escenarios: Debes crear {num_scene} escenarios con la estructura:

        Escenario 1: (Nombre del escenario)
        Descripción del escenario: (Detalles visuales y contextuales del escenario)

    - Portada
        Título: (Título del juego)
        Subtítulo: (Frase llamativa o resumen del propósito del juego)
        Imagen de fondo: (Descripción visual para la portada)
    - Menú Principal
        Título: (Título del juego)
        Introducción: (Frase que invite al jugador a adentrarse en la historia)
        Imagen de fondo: (Descripción visual del menú principal)

    - Capítulos
        Capítulo N
            Portada del Capítulo

            Indicación del capítulo: (Número del capítulo)
            Título del capítulo: (Nombre del capítulo)
            Introducción al capítulo: (Resumen de los eventos principales del capítulo)
            Imagen de fondo: (Descripción visual para la portada del capítulo)
            Objetivos pedagógicos: (Habilidades o aprendizajes que se esperan desarrollar en este capítulo)

            Pantalla de Contenido

            Imagen de fondo: (Descripción visual de la pantalla)
            Guión: (Diálogo o narración del capítulo) Ejemplo:
                - Personaje 1: ''.
                - Personaje 2: ''.
            Pantalla de Dinámicas

            Imagen de fondo: (Descripción visual de la dinámica)
            Pregunta: (Pregunta clave que enfrenta el jugador)
            Respuestas:
                (Opción correcta)
                (Opción incorrecta)
                (Opción incorrecta)
                (Opción incorrecta)
            Solución: (Explicación de por qué la opción correcta es la adecuada)

        Pantalla Final
            Imagen de fondo: (Descripción visual que simbolice el final del juego)
            Guión: (Diálogo final que cierre la narrativa del juego)

    </ESTRUCTURA>

    <CONTEXTO>
    {full_text}
    </CONTEXTO>

    """

    return full_prompt