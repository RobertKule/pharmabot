# -*- coding: utf-8 -*-
# main.py
# =========================
# PharmaBot Console
# =========================

"""
PharmaBot Console
Assistant d'orientation pharmaceutique en console

- LangChain v1+ (Runnable API)
- Modèle Gemini gratuit
- Mémoire de conversation en RAM
- Apprentissage "learn by doing"
"""

# =========================
# Imports de base
# =========================

from dotenv import load_dotenv

# Prompt structuré
from langchain_core.prompts import PromptTemplate

# Modèle Gemini (Google)
from langchain_google_genai import ChatGoogleGenerativeAI

# Prompt métier
from prompts import PHARMA_PROMPT


# =========================
# Imports mémoire (LangChain v1+)
# =========================

# Historique de conversation en RAM
from langchain_core.chat_history import InMemoryChatMessageHistory

# Wrapper pour ajouter la mémoire à une chain
from langchain_core.runnables.history import RunnableWithMessageHistory
# =========================
# Imports spécifiques LLM Google Gemini
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

# =========================
# Chargement des variables d'environnement
# =========================

# Charge GOOGLE_API_KEY depuis .env
load_dotenv()


# =========================
# Configuration du LLM
# =========================

# Gemini Flash : rapide, gratuit, suffisant pour ce projet
llm = ChatGoogleGenerativeAI(
    # model="gemini-2.5-flash",
    model="gemma-3-1b-it",
    temperature=0.3  # faible = réponses calmes et prudentes
)


# =========================
# Création du prompt
# =========================

# Le prompt reçoit :
# - symptoms : entrée utilisateur
# - history  : historique de la conversation
prompt = PromptTemplate(
    input_variables=["symptoms", "history"],
    template=PHARMA_PROMPT
)


# =========================
# Création de la chain de base
# =========================

# Prompt → LLM
base_chain = prompt | llm


# =========================
# Ajout de la mémoire
# =========================

# Historique stocké en RAM (session console)
chat_history = InMemoryChatMessageHistory()

# Chain avec mémoire
chain_with_memory = RunnableWithMessageHistory(
    base_chain,
    lambda session_id: chat_history,   # une seule session
    input_messages_key="symptoms",
    history_messages_key="history"
)


# =========================
# Fonction principale
# =========================

def get_pharma_advice(symptoms: str) -> str:
    """
    Envoie les symptômes à l'IA
    + conserve l'historique
    """
    try:
        response = chain_with_memory.invoke(
            {"symptoms": symptoms},
            config={
                "configurable": {
                    "session_id": "pharmabot_console"
                }
            }
        )
        return response.content
    except ChatGoogleGenerativeAIError as e:
        return "⚠️ Le quota gratuit du modèle Gemini est épuisé pour aujourd'hui. Veuillez réessayer plus tard ou envisager un plan payant."


# =========================
# Boucle console
# =========================

if __name__ == "__main__":

    print("🩺 PharmaBot Console")
    print("Tape 'exit' pour quitter\n")

    while True:
        user_input = input("👤 Décris tes symptômes : ")

        if user_input.lower() == "exit":
            print("👋 Au revoir!")
            break

        advice = get_pharma_advice(user_input)

        print("\n💊 PharmaBot :")
        print(advice)
        print("-" * 50)
