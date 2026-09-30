import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f172a 0%, #111827 40%, #1e293b 100%);
            font-family: 'Inter', sans-serif;
            color: #e5e7eb;
        }

        .stApp {
            background: transparent;
        }

        div[data-testid="stTitle"] {
            color: #f8fafc;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .stTextInput > div > div,
        .stTextArea > div > div,
        .stButton > button {
            border-radius: 14px;
        }

        .stTextArea textarea {
            background: rgba(15, 23, 42, 0.7);
            color: #f8fafc;
            border: 1px solid rgba(148, 163, 184, 0.35);
        }

        .stTextArea textarea::placeholder,
        .stTextInput input::placeholder {
            color: #cbd5e1;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select,
        .stNumberInput input {
            color: #f8fafc !important;
        }

        .stButton > button {
            background: linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%);
            color: #ffffff !important;
            border: none;
            font-weight: 600;
            padding: 0.7rem 1.2rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.35);
        }

        .stAlert, .stSuccess, .stWarning, .stError {
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
            color: #f8fafc !important;
        }

        .stMarkdown p,
        .stMarkdown li,
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4,
        .stMarkdown h5,
        .stMarkdown h6,
        .stMarkdown span {
            color: #f8fafc;
        }

        label,
        [data-testid="stWidgetLabel"],
        [data-testid="stHorizontalBlock"] {
            color: #f8fafc !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Gemini AI Chatbot", layout="centered")
st.title("Gemini AI Chatbot")
st.write("Ask Gemini anything!")

if not api_key:
    st.warning("Add your Gemini API key to a .env file as GEMINI_API_KEY=your_key or set it in your environment.")
    st.stop()

client = genai.Client(api_key=api_key)

prompt = st.text_area("Enter your prompt:", placeholder="Explain Artificial Intelligence in simple words...")

if st.button("Generate Response"):
    if prompt.strip():
        with st.spinner("Gemini is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                )
                result = getattr(response, "text", None)
                if result:
                    st.success("Response generated!")
                    st.write(result)
                else:
                    st.error("No response was returned. Please try again.")
            except Exception as e:
                st.error(
                    "Failed to connect to Gemini. Please check your API key, internet connection, and model access."
                )
                st.exception(e)
    else:
        st.warning("Please enter a prompt.")