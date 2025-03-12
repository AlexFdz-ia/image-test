import json
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_community.document_loaders import CSVLoader, PyPDFLoader

chat_history = []

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

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
)

# Definición del formulario
# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])

genre = st.text_input("Estilo de la obra: ", value="")
vibe = st.text_input("Tono de la novela: ", value="")
target = st.text_input("Público objetivo: ", value="")

col1, col2 = st.columns(2)
with col1:
    duration = st.number_input("Duración: ", min_value=0, value=0)
    num_characters = st.number_input("Número de personajes: ", min_value=0, value=0)
with col2:
    num_scene = st.number_input("Número de escenas: ", min_value=0, value=0)   
    num_chapters = st.number_input("Número de capítulos: ", min_value=0, value=0)

# Botón de envío
submit = st.button(label="Generar")

def check(genre, vibe, target, duration, num_characters, num_scene, num_chapters, uploaded_file):
    return (genre and vibe and target and duration and num_characters and num_scene and num_chapters and submit and uploaded_file)

if not check(genre, vibe, target, duration, num_characters, num_scene, num_chapters, uploaded_file):

    st.info("Por favor, rellena todos los campos", icon="ℹ️")

else:
    
    full_text = read_file(uploaded_file)

    # Establecemos la API de Google
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Seleccionamos el modelo a usar
    model = genai.GenerativeModel('gemini-1.5-flash')
