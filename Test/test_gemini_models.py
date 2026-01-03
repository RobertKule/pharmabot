# test_gemini_models.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Liste exhaustive des modèles récupérés depuis ta console
models_to_test = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-3-flash-preview",
    "gemini-3-pro-preview",
    "gemma-3-1b-it",
    "gemma-3-4b-it",
    "gemma-3-12b-it",
    "gemma-3-27b-it",
    "deep-research-pro-preview-12-2025"
]

def run_test():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Erreur : GOOGLE_API_KEY non trouvée dans le fichier .env")
        return

    print(f"🚀 Lancement des tests sur {len(models_to_test)} modèles...\n")

    for model_name in models_to_test:
        print(f"🔹 Test du modèle : {model_name}")
        try:
            # Configuration du modèle
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.1
            )
            
            # Appel du modèle (invoke remplace generate pour plus de simplicité)
            response = llm.invoke("Bonjour, réponds simplement 'OK' si tu fonctionnes.")
            
            print(f"✅ SUCCÈS")
            print(f"💬 Réponse : {response.content.strip()}\n")
            
        except Exception as e:
            print(f"❌ ÉCHEC pour {model_name}")
            # On affiche juste la première ligne de l'erreur pour garder la console propre
            print(f"⚠️  Raison : {str(e).splitlines()[0]}\n")

if __name__ == "__main__":
    run_test()