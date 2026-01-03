import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure()
listeId=[]
print("--- Modèles disponibles pour votre clé ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        # Affiche l'ID exact à copier dans votre code LangChain
        print(f"ID : {m.name.replace('models/', '')}  |  Nom : {m.display_name}")
        listeId.append(str(m.name.replace('models/', '')))
print("\n--- Fin de la liste des modèles ---")
print(f"\nTotal modèles avec génération de contenu : {len(listeId)}")
# Vous pouvez copier cette liste dans Test/test_gemini_models.py pour vos tests
print(listeId)
