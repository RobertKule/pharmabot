# -*- coding: utf-8 -*-
# utils.py
# =========================
# Détection simple de symptômes graves
# =========================

GRAVE_SYMPTOMS = [
    "douleur thoracique",
    "essoufflement",
    "saignement",
    "vomissements persistants",
    "fièvre élevée",
    "perte de conscience",
    "convulsions",
    "difficulté à respirer",
    "palpitations",
    "confusion"
]

def check_grave_symptoms(symptoms: str) -> bool:
    """
    Détecte des symptômes potentiellement graves.
    """
    text = symptoms.lower()
    return any(s in text for s in GRAVE_SYMPTOMS)
