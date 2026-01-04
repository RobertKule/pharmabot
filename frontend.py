# -*- coding: utf-8 -*-
# frontend.py
# =========================
# Interface simple PharmaBot
# =========================

import streamlit as st
from main import get_pharma_advice_with_history

# =========================
# Configuration page
# =========================

st.set_page_config(
    page_title="PharmaBot",
    page_icon="💊",
    layout="centered"
)

st.title("💊 PharmaBot")
st.write("Assistant d’orientation pharmaceutique (information générale uniquement).")

st.divider()

# =========================
# Mémoire UI (pas LLM)
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Affichage historique
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# Entrée utilisateur
# =========================

user_input = st.chat_input("Décris tes symptômes…")

if user_input:
    # afficher message utilisateur
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # réponse du bot
    with st.chat_message("assistant"):
        history_text = [
            f"Utilisateur: {m['content']}" if m["role"] == "user"
            else f"Assistant: {m['content']}"
            for m in st.session_state.messages
        ]

        response = get_pharma_advice_with_history(user_input, history_text)

        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
