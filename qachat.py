from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

# Configure API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Set page configuration
st.set_page_config(page_title="Q&A Demo", page_icon=":robot:")

# Custom CSS for improved styling
st.markdown("""
    <style>
    .main {
        background-color: #f4f4f4;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #333;
        color: #fff;
    }
    .stTextInput>div>input {
        border: 2px solid #007bff;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #007bff;
        color: #fff;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .chat-container {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
    }
    .chat-container .message {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
    }
    .chat-container .message.user {
        background-color: #d1ecf1;
        align-self: flex-end;
    }
    .chat-container .message.bot {
        background-color: #e2e3e5;
        align-self: flex-start;
    }
    .header-img {
        width: 50px;
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# Header with image
st.image("https://img.icons8.com/ios-filled/50/000000/robot.png", width=50)

st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input
input = st.text_input("Input: ", key="input", placeholder="Type your question here...")

# Submit button
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(["You", input])
    
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(["Bot", chunk.text])

st.subheader("The chat history is")

# Display chat history
for role, text in st.session_state['chat_history']:
    st.markdown(f'<div class="message {role.lower()}">{role}: {text}</div>', unsafe_allow_html=True)
