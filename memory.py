# -*- coding: utf-8 -*-
"""
Gestion de la mémoire conversationnelle pour PharmaBot.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

import logging
logger = logging.getLogger(__name__)

@dataclass
class Conversation:
    """Représente une conversation complète."""
    messages: List[Dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_message(self, role: str, content: str):
        """Ajoute un message à la conversation."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        self.updated_at = datetime.now().isoformat()
        logger.debug(f"Message ajouté: {role} - {content[:50]}...")
    
    def get_formatted_history(self) -> str:
        """Retourne l'historique formaté pour le prompt."""
        if not self.messages:
            return "Aucun historique précédent."
        
        formatted = []
        for msg in self.messages[-10:]:  # Garde les 10 derniers messages
            role = "Patient" if msg["role"] == "user" else "Pharmacien"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Retourne l'historique au format chat."""
        return self.messages.copy()

class ConversationManager:
    """Gère plusieurs conversations."""
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        logger.info("Gestionnaire de conversations initialisé")
    
    def create_conversation(self, session_id: str = "default") -> Conversation:
        """Crée une nouvelle conversation."""
        conversation = Conversation()
        self.conversations[session_id] = conversation
        logger.info(f"Nouvelle conversation créée: {session_id}")
        return conversation
    
    def get_conversation(self, session_id: str = "default") -> Conversation:
        """Récupère une conversation existante ou en crée une nouvelle."""
        if session_id not in self.conversations:
            return self.create_conversation(session_id)
        return self.conversations[session_id]
    
    def save_conversation(self, session_id: str, filepath: str):
        """Sauvegarde une conversation dans un fichier."""
        if session_id in self.conversations:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "session_id": session_id,
                    "conversation": self.conversations[session_id].__dict__
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Conversation sauvegardée: {filepath}")
    
    def load_conversation(self, filepath: str):
        """Charge une conversation depuis un fichier."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            conv = Conversation(**data["conversation"])
            self.conversations[data["session_id"]] = conv
            logger.info(f"Conversation chargée: {filepath}")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement: {e}")
            raise