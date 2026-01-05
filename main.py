# -*- coding: utf-8 -*-
"""
PharmaBot - Assistant d'orientation pharmaceutique.
Point d'entrée principal avec interface console.
"""

import sys
from typing import List, Optional
from colorama import init, Fore, Style

from models import PharmaModel
from memory import ConversationManager
from prompts import get_pharma_prompt
from utils import check_grave_symptoms, validate_user_input, format_chat_history, logger
import os
import dotenv

dotenv.load_dotenv()
# Initialisation colorama pour couleurs console
init(autoreset=True)
modelname = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")

class PharmaBot:
    """Classe principale de PharmaBot."""
    
    def __init__(self, model_name: str = str(modelname)):
        """
        Initialise PharmaBot.
        
        Args:
            model_name: Nom du modèle à utiliser
        """
        try:
            logger.info("Initialisation de PharmaBot...")
            
            # Initialisation des composants
            self.model_manager = PharmaModel(model_name=model_name)
            self.conversation_manager = ConversationManager()
            
            # Création de la chaîne de traitement
            prompt_template = get_pharma_prompt()
            self.chain = self.model_manager.create_chain(prompt_template)
            
            logger.info("PharmaBot initialisé avec succès")
            
        except Exception as e:
            logger.error(f"Échec de l'initialisation: {e}")
            print(f"{Fore.RED}Erreur d'initialisation: {e}")
            print(f"{Fore.YELLOW}Vérifiez votre fichier .env et votre connexion internet.")
            sys.exit(1)
    
    def get_pharma_advice(self, symptoms: str, session_id: str = "default") -> str:
        """
        Génère une réponse pour des symptômes donnés (sans historique).
        
        Args:
            symptoms: Description des symptômes
            session_id: ID de session pour la mémoire
            
        Returns:
            Réponse du bot
        """
        logger.info(f"Traitement de nouveaux symptômes: {symptoms[:50]}...")
        
        # Vérification des symptômes graves
        is_grave, alert_message = check_grave_symptoms(symptoms)
        if is_grave:
            logger.warning("Réponse d'urgence générée pour symptômes graves")
            return alert_message
        
        try:
            # Génération de la réponse
            response = self.chain.invoke({
                "symptoms": symptoms,
                "history": "Aucun historique précédent."
            })
            
            # Ajout à la mémoire
            conversation = self.conversation_manager.get_conversation(session_id)
            conversation.add_message("user", symptoms)
            conversation.add_message("assistant", response)
            
            logger.info("Réponse générée avec succès")
            return response
            
        except Exception as e:
            error_msg = f"Désolé, une erreur est survenue: {str(e)}"
            logger.error(f"Erreur lors de la génération: {e}")
            return error_msg
    
    def get_pharma_advice_with_history(self, symptoms: str, history: List[str], 
                                      session_id: str = "default") -> str:
        """
        Génère une réponse en tenant compte de l'historique.
        
        Args:
            symptoms: Nouveaux symptômes ou question
            history: Historique formaté de la conversation
            session_id: ID de session
            
        Returns:
            Réponse du bot avec contexte
        """
        logger.info(f"Traitement avec historique ({len(history)} messages)")
        
        # Vérification des symptômes graves
        is_grave, alert_message = check_grave_symptoms(symptoms)
        if is_grave:
            logger.warning("Réponse d'urgence générée pour symptômes graves")
            return alert_message
        
        try:
            # Formatage de l'historique
            formatted_history = format_chat_history(history)
            
            # Génération de la réponse
            response = self.chain.invoke({
                "symptoms": symptoms,
                "history": formatted_history
            })
            
            # Mise à jour de la mémoire
            conversation = self.conversation_manager.get_conversation(session_id)
            conversation.add_message("user", symptoms)
            conversation.add_message("assistant", response)
            
            logger.info("Réponse avec historique générée avec succès")
            return response
            
        except Exception as e:
            error_msg = "Désolé, je rencontre des difficultés techniques. Veuillez réessayer."
            logger.error(f"Erreur lors de la génération avec historique: {e}")
            return error_msg

def run_console_interface():
    """Interface console interactive pour PharmaBot."""
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN}💊 PHARMABOT - Assistant d'orientation pharmaceutique")
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.YELLOW}Version 2.0 - Interface Console Interactive")
    print(f"{Fore.WHITE}• Tapez 'exit' pour quitter")
    print(f"• Tapez 'clear' pour effacer l'historique")
    print(f"• Tapez 'history' pour voir la conversation")
    print(f"{Fore.CYAN}{'-'*60}\n")
    
    # Initialisation du bot
    bot = PharmaBot()
    
    # Gestion de la conversation
    conversation = bot.conversation_manager.create_conversation("console_session")
    chat_history = []
    
    while True:
        try:
            # Saisie utilisateur
            user_input = input(f"{Fore.GREEN}👤 Vous: {Style.RESET_ALL}")
            
            # Commandes spéciales
            if user_input.lower() == 'exit':
                print(f"{Fore.YELLOW}\n👋 Au revoir! Prenez soin de vous.")
                break
                
            elif user_input.lower() == 'clear':
                conversation = bot.conversation_manager.create_conversation("console_session")
                chat_history = []
                print(f"{Fore.BLUE}🗑️ Historique effacé.")
                continue
                
            elif user_input.lower() == 'history':
                print(f"{Fore.CYAN}\n📜 Historique de la conversation:")
                for msg in conversation.get_chat_history():
                    role = "Vous" if msg["role"] == "user" else "PharmaBot"
                    color = Fore.GREEN if msg["role"] == "user" else Fore.BLUE
                    print(f"{color}{role}: {msg['content'][:100]}...")
                print()
                continue
            
            # Validation de l'entrée
            is_valid, error_msg = validate_user_input(user_input)
            if not is_valid:
                print(f"{Fore.RED}❌ {error_msg}")
                continue
            
            # Préparation de l'historique pour le prompt
            history_for_prompt = []
            for msg in conversation.get_chat_history():
                role = "Utilisateur" if msg["role"] == "user" else "Assistant"
                history_for_prompt.append(f"{role}: {msg['content']}")
            
            # Affichage de l'attente
            print(f"{Fore.BLUE}💭 PharmaBot réfléchit...")
            
            # Génération de la réponse
            response = bot.get_pharma_advice_with_history(
                symptoms=user_input,
                history=history_for_prompt,
                session_id="console_session"
            )
            
            # Affichage de la réponse
            print(f"\n{Fore.BLUE}💊 PharmaBot: {Style.RESET_ALL}{response}")
            print(f"{Fore.CYAN}{'-'*60}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}\n🛑 Interruption. Tapez 'exit' pour quitter.")
            
        except Exception as e:
            logger.error(f"Erreur dans l'interface: {e}")
            print(f"{Fore.RED}❌ Une erreur est survenue. Veuillez réessayer.")

def main():
    """Point d'entrée principal."""
    try:
        run_console_interface()
    except Exception as e:
        logger.critical(f"Erreur critique: {e}")
        print(f"{Fore.RED}Une erreur critique est survenue. Le programme va s'arrêter.")
        sys.exit(1)

if __name__ == "__main__":
    main()