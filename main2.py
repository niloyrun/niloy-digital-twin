import streamlit as st
from PIL import Image
from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from dotenv import load_dotenv
import os


MODEL_NAME = "gemini-2.5-flash-lite"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key = st.secrets[GOOGLE_API_KEY]
gemini = OpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=google_api_key)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

if "messages" not in st.session_state:
    st.session_state.messages = []

def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]

    response = gemini.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,
    )

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)

        messages.append(message)
        messages.extend(results)

        response = gemini.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
        )

    return response.choices[0].message.content

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #001f3f;
    color: #ececef;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.avatar {
    width:160px;
    height:160px;
    border-radius:50%;
    object-fit:cover;
    border:3px solid #ecad0a;
    box-shadow:0 0 12px rgba(236,173,10,.6);
}

h1 {
    text-align: center;
    color: #209dd7;
}

.subtitle {
    text-align: center;
    color: #ecad0a;
    font-size: 20px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Niloy's Digital Twin",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    # ---------- Centered Photo ----------
    col1, col2 = st.columns([1, 3])

    with col2:
        import base64
        with open("niloy.png", "rb") as f:
            img = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <div style="text-align:center;">
            <img src="data:image/png;base64,{img}" class="avatar">
        </div>
        """, unsafe_allow_html=True)
    # ---------- HEADER ----------
    st.markdown("<h1>I'm Niloy's <em>digital twin</em>.</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Ask me anything — the real Niloy might just chime in.</div>", unsafe_allow_html=True)

    # ---------- INTRO TEXT ----------
    st.markdown("""
    I can answer questions about:

    - 💼 Career
    - 📊 Data Science
    - 🤖 AI Projects
    - 📈 Market Research
    - 🚁 FPV Drones
    - 💻 Python

    I can also help you get in touch directly or answer questions about his work.
    """)
    st.markdown("""
AI Engineer - Data Scientist - Market Research Expert
""")
    st.markdown("---")

    # ---------- FOOTER ----------
    st.markdown("""
    <center>
    © 2026 Niloy's Digital Twin | Powered by Streamlit <br>
    <a href="https://www.linkedin.com/in/niloy-banerjee-08368023/" target="_blank" style="color:#209dd7; text-decoration:none;">
    🔗 Connect on LinkedIn
    </a>
    </center>
    """, unsafe_allow_html=True)


left, center, right = st.columns([1, 2, 1])
with center:
    st.image("header.png")

# ---------- EXAMPLE PROMPTS ----------
st.markdown("#### Try asking:")
cols = st.columns(4)
example_prompt = None

if cols[0].button("🏏 Hobbies: What are your Hobbies?"):
    example_prompt = "What are your hobbies?"

elif cols[1].button("🧠 Skills: What are your strongest skills?"):
    example_prompt = "What are your strongest skills?"

elif cols[2].button("📞 Contact: How can I get in touch with you?"):
    example_prompt = "How can I get in touch with you?"

elif cols[3].button("💼 Experience: Tell me about your Market Research and Data Science background"):
    example_prompt = "Tell me about your Market Research and Data Science background"

# ---------- CHAT INPUT ----------
# ---------- Chat History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Chat Input ----------
typed_prompt = st.chat_input("Message Niloy's Twin...")

# Either typed text or clicked example
prompt = typed_prompt if typed_prompt else example_prompt

if prompt:

    # Save history BEFORE adding the current user message
    history = st.session_state.messages.copy()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat(prompt, history)

        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )


