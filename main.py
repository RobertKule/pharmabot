"""
PharmaBot Console
Assistant d'orientation pharmaceutique en console
- Utilise LangChain v1+ (Runnable)
- Modèle Gemini gratuit
- Mémoire de conversation en RAM
"""

# =========================
# Imports LangChain & utils
# =========================

# Pour créer un prompt structuré
from langchain_core.prompts import PromptTemplate

# Modèle Gemini (Google)
from langchain_google_genai import ChatGoogleGenerativeAI

# Chargement du prompt principal
from prompts import PHARMA_PROMPT

# Gestion des variables d'environnement (.env)
from dotenv import load_dotenv

# =========================
# Imports pour la mémoire
# =========================

# Historique de conversation en mémoire (RAM)
from langchain_core.chat_history import InMemoryChatMessageHistory

# Wrapper pour ajouter la mémoire à une chain Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory


# =========================
# Chargement des variables d'environnement
# =========================

# Charge GOOGLE_API_KEY depuis le fichier .env
load_dotenv()


# =========================
# Configuration du LLM
# =========================

# Initialisation du modèle Gemini
# temperature basse = réponses calmes, factuelles (important en santé)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


# =========================
# Création du prompt
# =========================

# PromptTemplate permet d'injecter dynamiquement les symptômes utilisateur
prompt = PromptTemplate(
    input_variables=["symptoms", "history"],
    template=PHARMA_PROMPT
)


# =========================
# Création de la chain LangChain (API moderne)
# =========================

# Ici on compose simplement :
# prompt -> LLM
chain = prompt | llm


# =========================
# Ajout de la mémoire
# =========================

# Stockage de l'historique de conversation en RAM
# (réinitialisé à chaque redémarrage du programme)
chat_history = InMemoryChatMessageHistory()

# On enveloppe la chain avec une mémoire conversationnelle
chain_with_memory = RunnableWithMessageHistory(
    chain,
    # Une fonction qui retourne l'historique selon l'id de session
    lambda session_id: chat_history,
    # Clé d'entrée utilisateur
    input_messages_key="symptoms",
    # Clé interne utilisée pour l'historique
    history_messages_key="history",
)


# =========================
# Fonction principale de réponse
# =========================

def get_pharma_advice(symptoms: str) -> str:
    """
    Envoie les symptômes à l'IA et retourne la réponse textuelle.
    La mémoire est automatiquement prise en compte.
    """
    response = chain_with_memory.invoke(
        {"symptoms": symptoms},
        # session_id permet de garder la même mémoire
        config={"configurable": {"session_id": "pharmabot_console"}}
    )
    return response.content


# =========================
# Boucle principale (console)
# =========================

if __name__ == "__main__":
    print("🩺 PharmaBot Console")
    print("Tape 'exit' pour quitter\n")

    while True:
        # Entrée utilisateur
        user_input = input("👤 Décris tes symptômes : ")

        # Condition de sortie
        if user_input.lower() == "exit":
            print("👋 Au revoir!")
            break

        # Appel de l'IA
        advice = get_pharma_advice(user_input)

        # Affichage de la réponse
        print("\n💊 PharmaBot :")
        print(advice)
        print("-" * 50)
