import streamlit as st
from functions import *
from img_functions import *

# Inicializa el `session_state` si aún no está inicializado
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.answer = ""
    st.session_state.result = ""
    st.session_state.query = ""
    st.session_state.images = []

# Show title and description.
st.title("📄 Crea tu propia novela")
st.write(
    "Sube un documento PDF y establece los valores para tu obra!"
)

# Definición del formulario
# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])

genre = st.text_input("Tipo de la obra: ", value="")
vibe = st.text_input("Tono de la novela: ", value="")
target = st.text_input("Público objetivo: ", value="")
style = st.text_input("Estilo de dibujo: ", value="")

col1, col2 = st.columns(2)
with col1:
    duration = st.number_input("Duración: ", min_value=0, value=0)
    num_characters = st.number_input("Número de personajes: ", min_value=0, value=0)
with col2:
    num_scene = st.number_input("Número de escenas: ", min_value=0, value=0)   
    num_chapters = st.number_input("Número de capítulos: ", min_value=0, value=0)

requirements = st.text_area("Requisitos:", max_chars=500, placeholder="Establecer diferentes especificaciones", height=250, value="""
250 caracteres con espacios incluidos (formato smartphone)
250 cc x caja Unas 3 cajas por imagen
Un personaje en la caja. Tres imágenes para la prueba
Ejemplo: Búsqueda de elementos en cuadros para resolver un asunto
policiaco Cada hallazgo da una pista para resolverlo. Lo hacemos con
tres cuadros del museo. Para la prueba es en orden.
Pero quisiera la opción de ponerle varias búsquedas y que las vaya
realizando el jugador hasta completarlo.
""")

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

            characters_dic = generate_characters(genre=genre, 
                                            vibe=vibe, 
                                            target=target, 
                                            num_characters=num_characters)

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

            img_prompts = create_img_prompts(characters=characters_dic, genre=genre, vibe=vibe, target=target, style=style)

            st.session_state.images = generate_images(prompts=img_prompts)

            i = 0
            for image in st.session_state.images:
                st.image(image, caption=characters_dic[i]["name"], use_container_width=True)
                i += 1

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

            characters_dic = generate_characters(genre=genre, 
                                            vibe=vibe, 
                                            target=target, 
                                            num_characters=num_characters)

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

            img_prompts = create_img_prompts(characters=characters_dic, genre=genre, vibe=vibe, target=target, style=style)

            st.session_state.images = generate_images(prompts=img_prompts)

            i = 0
            for image in st.session_state.images:
                st.image(image, caption=characters_dic[i]["name"], use_container_width=True)
                i += 1

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




    


    
