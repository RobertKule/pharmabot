# -*- coding: utf-8 -*-
# main.py
# =========================
# PharmaBot Console – INTERACTIF HUMAIN avec mémoire
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
# Init LLM et prompt
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
# Fonction principale
# =========================

def get_pharma_advice_with_history(symptoms: str, history: list[str]) -> str:
    """
    Génère une réponse humaine en utilisant l'historique complet.
    """
    try:
        if check_grave_symptoms(symptoms):
            return (
                "⚠️ Les symptômes décrits peuvent être sérieux.\n"
                "Il est important de consulter rapidement un professionnel de santé.\n"
                "on a fini. As-tu d'autres questions ?"
            )

        formatted_history = "\n".join(history)

        response = base_chain.invoke({
            "symptoms": symptoms,
            "history": formatted_history
        })

        return response.content

    except ChatGoogleGenerativeAIError:
        return "⚠️ Le quota du modèle est atteint. Réessaie plus tard."

# =========================
# Interface console
# =========================

if __name__ == "__main__":
    print("🩺 PharmaBot Console – INTERACTIF HUMAIN")
    print("Tape 'exit' pour quitter\n")

    chat_memory = []

    while True:
        user_input = input("👤 Décris tes symptômes : ")
        if user_input.lower() == "exit":
            print("👋 Au revoir!")
            break

        chat_memory.append(f"Utilisateur : {user_input}")

        response = get_pharma_advice_with_history(user_input, chat_memory)

        chat_memory.append(f"Assistant : {response}")

        print("\n💊 PharmaBot :")
        print(response)
        print("-" * 50)
