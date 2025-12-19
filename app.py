import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from personalities import PERSONALITIES

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Agent Chatbot", layout="centered")
st.title("🤖 AI Agent Chatbot")

with st.sidebar:
    personality = st.selectbox(
        "Select Personality",
        list(PERSONALITIES.keys())
    )

    model = st.selectbox(
        "Select Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile"
        ]
    )

    st.caption(PERSONALITIES[personality]["description"])

system_prompt = PERSONALITIES[personality]["system_prompt"]

if (
    "messages" not in st.session_state
    or st.session_state.get("personality") != personality
):
    st.session_state.personality = personality
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:
            st.error(f"Error: {e}")
