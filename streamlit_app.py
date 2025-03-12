import streamlit as st
from functions import *

chat_history = []

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

requirements = st.text_area("Requisitos:", max_chars=500, placeholder="Establecer diferentes especificaciones")

# Botón de envío
submit = st.button(label="Generar")

if not check(genre=genre, 
      vibe=vibe, 
      target=target, 
      duration=duration, 
      num_characters=num_characters,
      num_scene=num_scene,
      num_chapters=num_chapters,
      submit=submit,
      requirements=requirements,
      uploaded_file=uploaded_file):

    st.info("Por favor, rellena todos los campos", icon="ℹ️")

else:
    
    full_text = read_file(uploaded_file=uploaded_file)

    characters_dic = generate_characters(genre=genre, vibe=vibe, target=target, num_characters=num_characters)

    prompt = generate_prompt(genre=genre, 
                             vibe=vibe, 
                             target=target, 
                             duration=duration, 
                             num_scene=num_scene, 
                             num_chapters=num_chapters, 
                             requirements=requirements, 
                             full_text=full_text, 
                             characters_dic=characters_dic)
    
    answer = generate_answer(chat_history=chat_history, prompt=prompt)

    st.text_area(value=answer)

    query = st.text_input("¿Realizar alguna pregunta?")
    question = st.button("Preguntar")

    if query and question:
        result = generate_answer(prompt=query, chat_history=chat_history)
        st.text_area(value=result)


    
