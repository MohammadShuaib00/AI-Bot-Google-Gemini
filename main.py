import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (
    load_gemini_pro_model, gemini_pro_vision_response, embedding_model_response, gemini_pro_response)
from PIL import Image

working_directory = os.path.dirname(os.path.abspath(__file__))

# Setting up the page configuration
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🧠",
    layout="centered"
)

# Sidebar configuration with the option menu
with st.sidebar:
    selected = option_menu(
        "Gemini AI",
        ['ChatBot', 'Image Captioning', 'Embed Text', 'Ask me anything'],
        icons=['bi-chat-dots-fill', 'image-fill',
               'textarea-t', 'patch-question-fill'],
        menu_icon='robot',
        default_index=0
    )

# Function to translate role between gemini-pro and streamlit


def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return "assistant"
    else:
        return user_role


# Add your code to handle the selected option here
if selected == "ChatBot":
    model = load_gemini_pro_model()

    # Initialize chat session in streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit page title
    st.title("🤖 AI ChatBot")

    # Display chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(
            user_prompt)

        # Display the Gemini-Pro response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

elif selected == "Image Captioning":
    # streamlit page title
    st.title("📷 Snap Narrate")

    uploaded_image = st.file_uploader(
        "Upload an Image....", type=["jpg", "jpeg", "png"])

    if st.button('Generate Caption'):
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resize_image = image.resize((800, 500))
            st.image(resize_image)

        default_prompt = "write a short caption for this image"

        # getting the response form gemini-pro-vision-model
        caption = gemini_pro_vision_response(default_prompt, image)
        with col2:
            st.info(caption)

elif selected == "Embed Text":
    st.title("🔡 Embedded Text.....")

    # input text box
    input_text = st.text_area(
        label="", placeholder="Enter the text to get the embedding...")
    if st.button("Get Embedding.."):
        response = embedding_model_response(input_text)
        st.markdown(response)

elif selected == "Ask me anything":
    st.title("❓ Ask me anything...")

    # text box to enter prompt
    user_prompt = st.text_area(label="", placeholder="Ask Gemini Pro..")

    if st.button("Get an answer"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)
