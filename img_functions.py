import base64, json
import streamlit as st
from together import Together
from io import BytesIO
from PIL import Image

TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
client=Together(api_key=TOGETHER_API_KEY)

def create_img_prompts(characters, genre, vibe, target, style):
    prompts = []

    for character in characters:

        prompt = f"""
        The background MUST be WHITE and completely REMOVED. YOU CANT CROP ANYTHING from the character {style} style.
        ENSURE that the character's FULL-BODY character is facing FORWARD AND is fully VISIBLE without CROPPING any part, including the character's HAIR.
        The character (character name: {character["name"]}) is from a visual novel should embody the following description: {character["visual_description"]}. And also the following personality traits: {character["personality_traits"]}
        The art style and design should align with the novel genre {genre}, evoking the novel tone {vibe}, and appealing directly to the intended audience {target}.
        The background MUST be WHITE and completely REMOVED.
        """

        prompts.append(prompt)
        
    return prompts

def generate_images(prompts):

  images = []

  for prompt in prompts:

    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=1024,
        height=768,
        steps=4,
        n=1,
        response_format="b64_json"
        )

    img = Image.open(BytesIO(base64.b64decode(response.data[0].b64_json)))

    images.append(img)

  return images
