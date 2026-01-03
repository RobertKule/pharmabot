# test_gemini_models.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()



models_to_test=[
    'gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash-exp', 'gemini-2.0-flash', 
    'gemini-2.0-flash-001', 'gemini-2.0-flash-exp-image-generation', 'gemini-2.0-flash-lite-001', 
    'gemini-2.0-flash-lite', 'gemini-2.0-flash-lite-preview-02-05', 'gemini-2.0-flash-lite-preview', 
    'gemini-exp-1206', 'gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts', 'gemma-3-1b-it', 
    'gemma-3-4b-it', 'gemma-3-12b-it', 'gemma-3-27b-it', 'gemma-3n-e4b-it', 'gemma-3n-e2b-it', 
    'gemini-flash-latest', 'gemini-flash-lite-latest', 'gemini-pro-latest', 'gemini-2.5-flash-lite', 
    'gemini-2.5-flash-image-preview', 'gemini-2.5-flash-image', 'gemini-2.5-flash-preview-09-2025', 
    'gemini-2.5-flash-lite-preview-09-2025', 'gemini-3-pro-preview', 'gemini-3-flash-preview', 
    'gemini-3-pro-image-preview', 'nano-banana-pro-preview', 'gemini-robotics-er-1.5-preview', 
    'gemini-computer-use-preview-tts']
models_to_test = list(set(models_to_test))  # Supprime les doublons éventuels

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