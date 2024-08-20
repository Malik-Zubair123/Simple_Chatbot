import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Configure the API key
api_key = os.getenv("api_key")
genai.configure(api_key=api_key)

# Initialize the model once and store it in session state
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from model
def getResponseFromModel(user_input):
    response = st.session_state.model.generate_content(user_input)
    return response.text

# Set page configuration
st.set_page_config(
    page_title="Simple Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Main title and description
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Simple Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #808080;'>Used by Google Gemini API</p>", unsafe_allow_html=True)

# Initialize chat history if not already present
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history above the chat form
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)
for i, chat in enumerate(st.session_state.chat_history):
    st.markdown(f"<div style='background-color:#f9f9f9; color:#333; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
                f"<strong>You:</strong> {chat['user']}</div>", unsafe_allow_html=True)
    if i < len(st.session_state.chat_history) - 1:  # Display response only for previous chats
        st.markdown(f"<div style='background-color:#e3f2fd; color:#0066cc; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>"
                    f"<strong>Model:</strong> {chat['response']}</div>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc;'>", unsafe_allow_html=True)

# Create a form for user input
form = st.form(key='chat_form', clear_on_submit=True)
user_input = form.text_input("Enter query Dear :", key="user_input", placeholder="Type your question here...", help="Enter your query and press 'Send'")
submit_button = form.form_submit_button("Send")

# Handle form submission
if submit_button and user_input:
    with st.spinner('Processing...'):
        output = getResponseFromModel(user_input)
        st.session_state.chat_history.append({'user': user_input, 'response': output})

        # Display the latest user query and response immediately
        st.markdown(f"<div style='background-color:#f9f9f9; color:#333; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>"
                    f"<strong>You:</strong> {user_input}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color:#e3f2fd; color:#0066cc; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>"
                    f"<strong>Model:</strong> {output}</div>", unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #808080;'>© 2024 Chatbot by Malik Muhammad Zubair</p>", unsafe_allow_html=True)