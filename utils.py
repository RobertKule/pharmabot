# -*- coding: utf-8 -*-
"""
Utilitaires pour PharmaBot - Détection de symptômes graves et fonctions auxiliaires.
"""

import logging
from typing import List, Tuple

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Symptômes graves nécessitant une consultation immédiate
GRAVE_SYMPTOMS = [
    "douleur thoracique", "douleur poitrine", "douleur thorax",
    "essoufflement", "souffle court", "respiration difficile",
    "saignement abondant", "hémorragie", "saigne beaucoup",
    "vomissements incoercibles", "vomissements persistants",
    "fièvre > 40", "fièvre très élevée", "hyperthermie",
    "perte de conscience", "syncope", "évanouissement",
    "convulsions", "crise convulsive",
    "difficulté à respirer", "respiration sifflante",
    "palpitations fortes", "cœur qui bat très vite",
    "confusion mentale", "désorientation",
    "paralysie", "faiblesse soudaine",
    "maux de tête violents", "céphalée intense"
]

# Symptômes nécessitant une consultation sous 24h
URGENT_SYMPTOMS = [
    "fièvre > 38.5", "fièvre persistante",
    "douleur intense", "douleur insupportable",
    "vomissements fréquents", "diarrhée abondante",
    "brûlure étendue", "coupure profonde",
    "réaction allergique", "urticaire",
    "essoufflement modéré"
]

def check_grave_symptoms(symptoms: str) -> Tuple[bool, str]:
    """
    Détecte des symptômes potentiellement graves.
    
    Args:
        symptoms: Description des symptômes par l'utilisateur
        
    Returns:
        Tuple (is_grave, message): Si grave et message d'alerte approprié
    """
    text = symptoms.lower()
    
    # Détection symptômes graves (consultation immédiate)
    for symptom in GRAVE_SYMPTOMS:
        if symptom in text:
            logger.warning(f"Symptôme grave détecté: {symptom}")
            return True, (
                "⚠️ **URGENCE MÉDICALE**\n\n"
                "Les symptômes que vous décrivez nécessitent une consultation IMMÉDIATE.\n"
                "Veuillez contacter le SAMU (15) ou vous rendre aux urgences.\n\n"
                "on a fini. As-tu d'autres questions ?"
            )
    
    # Détection symptômes urgents (consultation sous 24h)
    for symptom in URGENT_SYMPTOMS:
        if symptom in text:
            logger.info(f"Symptôme urgent détecté: {symptom}")
            return False, (
                "🔸 **Consultez rapidement**\n\n"
                "Vos symptômes nécessitent une consultation médicale dans les 24 heures.\n"
                "Prenez rendez-vous avec votre médecin ou allez à la maison médicale de garde.\n\n"
                "on a fini. As-tu d'autres questions ?"
            )
    
    return False, ""

def format_chat_history(history: List[str]) -> str:
    """
    Formate l'historique de conversation pour le prompt.
    
    Args:
        history: Liste des messages (user/assistant)
        
    Returns:
        Historique formaté
    """
    if not history:
        return "Aucun historique précédent."
    
    formatted = []
    for i, message in enumerate(history, 1):
        formatted.append(f"{i}. {message}")
    
    return "\n".join(formatted)

def validate_user_input(input_text: str) -> Tuple[bool, str]:
    """
    Valide l'entrée utilisateur.
    
    Args:
        input_text: Texte saisi par l'utilisateur
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not input_text or not input_text.strip():
        return False, "Veuillez décrire vos symptômes."
    
    if len(input_text.strip()) < 3:
        return False, "La description est trop courte."
    
    if len(input_text) > 1000:
        return False, "La description est trop longue (max 1000 caractères)."
    
    return True, ""