import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
)

# Definición del formulario
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

def check(genre, vibe, target, duration, num_characters, num_scene, num_chapters):
    return (genre and vibe and target and duration and num_characters and num_scene and num_chapters and submit)

if not check(genre, vibe, target, duration, num_characters, num_scene, num_chapters):
    st.info("Por favor, rellena todos los campos", icon="ℹ️")
else:
    st.write("hola")
