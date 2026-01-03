# -*- coding: utf-8 -*-
# main.py
# =========================
# PharmaBot Console – INTERACTIF HUMAIN
# =========================

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

from prompts import PHARMA_PROMPT
from utils import check_grave_symptoms

# =========================
# Init
# =========================

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemma-3-1b-it",
    temperature=0.3
)

prompt = PromptTemplate(
    input_variables=["symptoms", "history"],
    template=PHARMA_PROMPT
)

base_chain = prompt | llm

chat_history = InMemoryChatMessageHistory()

chain = RunnableWithMessageHistory(
    base_chain,
    lambda session_id: chat_history,
    input_messages_key="symptoms",
    history_messages_key="history"
)

# =========================
# Logique principale
# =========================

def get_pharma_advice(symptoms: str) -> str:
    """
    Gère une interaction humaine avec mémoire.
    """
    try:
        # Détection urgence AVANT LLM
        if check_grave_symptoms(symptoms):
            return (
                "⚠️ Les symptômes décrits peuvent être sérieux.\n"
                "Il est important de consulter rapidement un professionnel de santé.\n"
                "on a fini. As-tu d'autres questions ?"
            )

        response = chain.invoke(
            {"symptoms": symptoms},
            config={"configurable": {"session_id": "pharmabot_console"}}
        )

        return response.content

    except ChatGoogleGenerativeAIError:
        return "⚠️ Le quota du modèle est atteint. Réessaie plus tard."

# =========================
# Console
# =========================

if __name__ == "__main__":
    print("🩺 PharmaBot Console")
    print("Tape 'exit' pour quitter\n")

    while True:
        user_input = input("👤 Décris tes symptômes : ")

        if user_input.lower() == "exit":
            print("👋 Au revoir!")
            break

        print("\n💊 PharmaBot :")
        print(get_pharma_advice(user_input))
        print("-" * 50)
