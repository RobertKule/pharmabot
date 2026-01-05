# -*- coding: utf-8 -*-
"""
Gestion des modèles LLM pour PharmaBot.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import logging
logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

modelname = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")
class PharmaModel:
    """Classe pour gérer le modèle LLM et la chaîne de traitement."""
    
    def __init__(self, model_name: str = str(modelname), temperature: float = 0.2):
        """
        Initialise le modèle LLM.
        
        Args:
            model_name: Nom du modèle Google Generative AI
            temperature: Créativité du modèle (0-1)
        """
        load_dotenv()
        
        if not os.getenv("GOOGLE_API_KEY"):
            logger.error("GOOGLE_API_KEY non trouvée dans les variables d'environnement")
            raise ValueError(
                "Veuillez définir GOOGLE_API_KEY dans le fichier .env\n"
                "Exemple: GOOGLE_API_KEY=votre_cle_api_ici"
            )
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_output_tokens=1024,
                timeout=30,
                max_retries=2
            )
            logger.info(f"Modèle {model_name} initialisé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du modèle: {e}")
            raise
    
    def create_chain(self, prompt_template: str):
        """
        Crée une chaîne de traitement LangChain.
        
        Args:
            prompt_template: Template du prompt
            
        Returns:
            Chaîne LangChain configurée
        """
        prompt = PromptTemplate(
            input_variables=["symptoms", "history"],
            template=prompt_template
        )
        
        chain = prompt | self.llm | StrOutputParser()
        return chain