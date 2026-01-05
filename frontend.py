# -*- coding: utf-8 -*-
"""
Interface PharmaBot - Design professionnel et minimaliste
"""

import streamlit as st
import sys
import os

# Ajout du chemin courant pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import PharmaBot
from utils import check_grave_symptoms, validate_user_input

# Configuration de la page
st.set_page_config(
    page_title="PharmaBot",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation session state
if "bot" not in st.session_state:
    st.session_state.bot = PharmaBot()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

# CSS professionnel avec design accessible
st.markdown("""
<style>
    /* Styles globaux */
    .main {
        padding: 2rem 1rem;
    }
    
    /* Messages utilisateur */
    .user-message {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 16px 16px 4px 16px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0 1rem auto;
        max-width: 85%;
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
    
    /* Messages bot */
    .bot-message {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        border-radius: 16px 16px 16px 4px;
        padding: 1.2rem 1.5rem;
        margin: 1rem auto 1rem 0;
        max-width: 85%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
    }
    
    /* Messages urgents */
    .urgent-message {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        color: #fed7d7;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 2px solid #fca5a5;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
        animation: pulse 2s infinite;
        max-width: 90%;
    }
    
    /* Animation pour messages urgents */
    @keyframes pulse {
        0% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 4px 30px rgba(239, 68, 68, 0.5); }
        100% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
    }
    
    /* Badges d'avatar */
    .user-message::before {
        content: '👤';
        position: absolute;
        left: -45px;
        top: 50%;
        transform: translateY(-50%);
        background: #1e3c72;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 2px solid white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .bot-message::before {
        content: '💊';
        position: absolute;
        right: -45px;
        top: 50%;
        transform: translateY(-50%);
        background: #2d3748;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 2px solid white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Container principal */
    .chat-container {
        max-height: 65vh;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 2rem;
        border-radius: 12px;
        background: #0f172a;
        border: 1px solid #334155;
    }
    
    /* Scrollbar personnalisée */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Zone de saisie améliorée */
    .stChatInput > div > div {
        background: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }
    
    .stChatInput input {
        color: white !important;
        font-size: 1rem !important;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: #0f172a;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #3b82f6 transparent transparent transparent !important;
    }
    
    /* Titres */
    h1 {
        color: #3b82f6 !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Tooltips et info */
    .stAlert {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar professionnelle
with st.sidebar:
    # Logo et titre
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">💊</div>
        <h2 style="color: #3b82f6; margin: 0;">PharmaBot</h2>
        <p style="color: #94a3b8; font-size: 0.9rem;">Assistant d'orientation pharmaceutique</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Informations
    with st.expander("ℹ️ À propos", expanded=True):
        st.markdown("""
        **PharmaBot** vous aide à comprendre vos symptômes et vous oriente vers les bonnes ressources.
        
        ⚠️ **Important :**
        - Ne remplace pas une consultation médicale
        - Pas de diagnostic ni d'ordonnance
        - Pour orientation générale uniquement
        """)
    
    st.markdown("---")
    
    # Gestion de la conversation
    st.markdown("### 📝 Gestion")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Effacer", help="Effacer l'historique de la conversation"):
            st.session_state.messages = []
            st.session_state.history = []
            st.rerun()
    with col2:
        if st.button("📋 Exporter", help="Exporter la conversation"):
            st.info("Fonctionnalité d'export à venir")
    
    st.markdown("---")
    
    # Urgences
    st.markdown("### 🚨 Urgences")
    with st.expander("Numéros d'urgence", expanded=True):
        st.markdown("""
        **SAMU (Urgences médicales)**
        ```
        📞 15
        ```
        
        **Pharmacie de garde**
        ```
        📞 3237
        ```
        
        **Pompiers**
        ```
        📞 18
        ```
        
        **Urgences européennes**
        ```
        📞 112
        ```
        """)

# Header principal
col1, col2, col3 = st.columns([2, 3, 1])
with col1:
    st.markdown("### 💬 Conversation")
with col3:
    st.caption(f"Messages: {len(st.session_state.messages)}")

st.markdown("---")

# Container de chat avec scroll
chat_container = st.container()

with chat_container:
    # Container interne pour le scroll
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #94a3b8;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">💊</div>
            <h3 style="color: #e2e8f0; margin-bottom: 1rem;">Bienvenue sur PharmaBot</h3>
            <p>Décrivez vos symptômes pour recevoir des conseils d'orientation.</p>
            <p style="font-size: 0.9rem; margin-top: 2rem;">
                Exemple : <em>"J'ai mal à la tête depuis ce matin et je me sens fatigué"</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="user-message">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                css_class = "urgent-message" if "⚠️" in message["content"] else "bot-message"
                st.markdown(
                    f'<div class="{css_class}">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Zone de saisie améliorée
# st.markdown("---")
user_input = st.chat_input(
    "Décrivez vos symptômes ou posez une question...",
    key="chat_input"
)

if user_input:
    # Validation
    is_valid, error_msg = validate_user_input(user_input)
    
    if not is_valid:
        st.toast(f"⚠️ {error_msg}", icon="⚠️")
    else:
        # Ajout du message utilisateur avec feedback
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.history.append(f"Utilisateur: {user_input}")
        
        # Génération de la réponse avec indicateur visuel
        with st.spinner("💭 PharmaBot analyse votre demande..."):
            try:
                # Vérification symptômes graves
                is_grave, alert_message = check_grave_symptoms(user_input)
                
                if is_grave:
                    response = alert_message
                    st.toast("⚠️ Symptômes graves détectés - Urgence médicale", icon="🚨")
                else:
                    # Préparation historique pour le prompt
                    history_for_prompt = st.session_state.history[-10:] if st.session_state.history else []
                    
                    # Génération de la réponse
                    response = st.session_state.bot.get_pharma_advice_with_history(
                        symptoms=user_input,
                        history=history_for_prompt
                    )
                    st.toast("✅ Réponse générée avec succès", icon="✅")
                
                # Ajout de la réponse
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.history.append(f"Assistant: {response}")
                
                # Rechargement pour affichage
                st.rerun()
                
            except Exception as e:
                st.toast("❌ Erreur lors de la génération", icon="❌")
                error_msg = "Désolé, une erreur technique est survenue. Veuillez réessayer."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.rerun()

# # Pied de page discret
# st.markdown("---")
# st.markdown(
#     """
#     <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
#         <p>⚠️ <strong>Important :</strong> PharmaBot fournit des conseils d'orientation générale uniquement.<br>
#         Consultez toujours un professionnel de santé pour un diagnostic et un traitement appropriés.</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )