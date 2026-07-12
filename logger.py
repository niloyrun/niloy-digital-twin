import requests
import streamlit as st


def log_chat(question, answer, email="", phone=""):

    requests.post(
        st.secrets["GOOGLE_SCRIPT_URL"],
        json={
            "question": question,
            "answer": answer,
            "email": email,
            "phone": phone
        },
        timeout=5
    )
