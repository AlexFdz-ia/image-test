import streamlit as st
from functions import *

# Inicializa el `session_state` si aún no está inicializado
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.answer = ""
    st.session_state.result = ""
    st.session_state.query = ""

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – Gemini will answer! "
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

requirements = st.text_area("Requisitos:", max_chars=500, placeholder="Establecer diferentes especificaciones", height=250)

# Botón de envío
submit = st.button(label="Generar")

if not st.session_state.chat_history:

    if submit:

        if not check(genre=genre, 
            vibe=vibe, 
            target=target, 
            duration=duration, 
            num_characters=num_characters,
            num_scene=num_scene,
            num_chapters=num_chapters,
            # submit=submit,
            requirements=requirements,
            uploaded_file=uploaded_file):

            st.info("Por favor, rellena todos los campos", icon="ℹ️")

        else:
            
            full_text = read_file(file=uploaded_file)

            characters = generate_characters(genre=genre, 
                                            vibe=vibe, 
                                            target=target, 
                                            num_characters=num_characters)
            
            st.text(characters)
            
            characters_dic = json.loads(characters)

            prompt = generate_prompt(genre=genre, 
                                    vibe=vibe, 
                                    target=target, 
                                    duration=duration, 
                                    num_scene=num_scene, 
                                    num_chapters=num_chapters, 
                                    requirements=requirements, 
                                    full_text=full_text, 
                                    characters_dic=characters_dic)
            
            st.session_state.answer = generate_answer(chat_history=st.session_state.chat_history, prompt=prompt)

            st.text_area("Respuesta: ", st.session_state.answer, height=800)

            st.session_state.query = st.text_input("¿Realizar alguna pregunta?")
            question = st.button("Preguntar")

            if st.session_state.query and question:
                st.session_state.result = generate_answer(prompt=st.session_state.query, chat_history=st.session_state.chat_history)

else:

    if submit:

        if not check(genre=genre, 
            vibe=vibe, 
            target=target, 
            duration=duration, 
            num_characters=num_characters,
            num_scene=num_scene,
            num_chapters=num_chapters,
            # submit=submit,
            requirements=requirements,
            uploaded_file=uploaded_file):

            st.info("Por favor, rellena todos los campos", icon="ℹ️")

        else:
            
            full_text = read_file(file=uploaded_file)

            characters = generate_characters(genre=genre, 
                                            vibe=vibe, 
                                            target=target, 
                                            num_characters=num_characters)
            
            st.text(characters)
            
            characters_dic = json.loads(characters)

            prompt = generate_prompt(genre=genre, 
                                    vibe=vibe, 
                                    target=target, 
                                    duration=duration, 
                                    num_scene=num_scene, 
                                    num_chapters=num_chapters, 
                                    requirements=requirements, 
                                    full_text=full_text, 
                                    characters_dic=characters_dic)
            
            st.session_state.answer = generate_answer(chat_history=st.session_state.chat_history, prompt=prompt)

    st.text_area("Respuesta: ", st.session_state.answer, height=800)

    query2 = st.text_input("¿Realizar alguna pregunta?")
    question2 = st.button("Preguntar")

    if query2 and question2:
        st.session_state.result = generate_answer(prompt=query2, chat_history=st.session_state.chat_history)

    text_len = len(st.session_state.result)
    if text_len < 50:
        st.text_area("Respuesta: ", st.session_state.result)
    elif text_len < 500:
        st.text_area("Respuesta: ", st.session_state.result, height=250)
    else:
        st.text_area("Respuesta: ", st.session_state.result, height=800)




    


    
