import os
import streamlit as st
import json
import google.generativeai as genai
from PIL import Image, ImageFilter


working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f"{working_directory}/config.json"

config_data = json.load(open(config_file_path))

# loading the api key
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

# configuring google generativeai with api key
genai.configure(api_key=GOOGLE_API_KEY)


def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# function for image captioning


def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel(
        "gemini-pro-vision")  # Corrected argument name
    response = gemini_pro_vision_model.generate_content(image)
    return response.text

# function to get embedding for text


def embedding_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(
        model=embedding_model, content=input_text, task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list


# function to get a response from gemini-pro LLM
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel('gemini-pro')
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
