import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- Modèles disponibles pour votre clé ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        # Affiche l'ID exact à copier dans votre code LangChain
        print(f"ID : {m.name.replace('models/', '')}  |  Nom : {m.display_name}")