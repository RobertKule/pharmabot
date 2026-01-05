# 💊 PharmaBot - Assistant d'Orientation Pharmaceutique

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0.0-green.svg)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**PharmaBot** est un assistant conversationnel intelligent spécialisé dans l'orientation pharmaceutique. Il aide les utilisateurs à comprendre leurs symptômes et les guide vers les bonnes ressources médicales, sans jamais remplacer un professionnel de santé.

---

## 🎯 Fonctionnalités Principales

### 🤖 Assistant Intelligent
- **Conversation naturelle** avec mémoire contextuelle
- **Compréhension des symptômes** et analyse en temps réel
- **Reformulation humaine** des problèmes médicaux
- **Conseils pratiques** adaptés à chaque situation
- **Détection automatique** des symptômes graves nécessitant une urgence

### 🛡️ Sécurité & Éthique
- ❌ **Aucun diagnostic médical**
- ❌ **Aucune prescription de médicaments**
- ✅ **Orientation vers les bonnes ressources**
- ✅ **Recommandation de consulter un professionnel**
- ✅ **Messages d'alerte pour les urgences médicales**

### 💻 Interfaces Disponibles
- **Interface Console** : Pour un usage rapide et technique
- **Interface Web (Streamlit)** : Interface moderne et intuitive

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.9 ou supérieur
- Clé API Google Gemini ([Obtenir une clé ici](https://makersuite.google.com/app/apikey))

### Installation en 3 étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/RobertKule/pharmabot.git
cd pharmabot
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer l'environnement**
```bash
echo "GOOGLE_API_KEY=votre_cle_api_ici" > .env
```

---

## 🎮 Utilisation

### Interface Console
```bash
python main.py
```
**Commandes disponibles :**
- `exit` : Quitter l'application
- `clear` : Effacer l'historique
- `history` : Afficher les 10 derniers messages
- `help` : Afficher l'aide

### Interface Web
```bash
streamlit run frontend.py
```
Ouvrez votre navigateur à l'adresse : `http://localhost:8501`

---

## 📁 Structure du Projet

```
pharmabot/
├── .env                    # Variables d'environnement
├── .gitignore             # Fichiers ignorés par Git
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation (ce fichier)
├── main.py               # Application console principale
├── prompts.py            # Templates de prompts optimisés
├── utils.py              # Fonctions utilitaires
├── frontend.py           # Interface web Streamlit
└── assets/               # Ressources visuelles
```

### 🧠 Architecture Technique

```
┌─────────────────────────────────────────────────┐
│                   Interface                      │
│         (Console / Web Streamlit)                │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Contrôleur PharmaBot               │
│    • Gestion mémoire conversationnelle          │
│    • Validation des entrées utilisateur         │
│    • Détection symptômes graves                 │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Modèle LangChain                    │
│    • ChatGoogleGenerativeAI (Gemini)            │
│    • PromptTemplate optimisé                    │
│    • Gestion du contexte historique             │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Configuration Avancée

### Variables d'environnement
```bash
# .env
GOOGLE_API_KEY=votre_cle_api_ici
MODEL_NAME=gemini-pro          # gemini-pro, gemini-1.5-pro, etc.
TEMPERATURE=0.2                # Créativité du modèle (0-1)
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
```

### Personnalisation du prompt
Modifiez `prompts.py` pour adapter le comportement du bot :
```python
PHARMA_PROMPT_TEMPLATE = """
Tu es PharmaBot, un assistant d'orientation pharmaceutique...
# Votre prompt personnalisé ici
"""
```

### Ajout de symptômes graves
Modifiez `utils.py` pour ajouter vos propres critères :
```python
GRAVE_SYMPTOMS = [
    "douleur thoracique",
    "essoufflement",
    # Ajoutez vos symptômes ici
]
```

---

## 📊 Exemples d'Utilisation

### Cas 1 : Symptômes courants
```
👤 Utilisateur : J'ai mal à la tête depuis ce matin

💊 PharmaBot : Je comprends que vous avez des maux de tête depuis ce matin...
→ Conseils sur l'hydratation et le repos
→ Recommandation de consulter si les symptômes persistent
→ on a fini. As-tu d'autres questions ?
```

### Cas 2 : Symptômes graves
```
👤 Utilisateur : J'ai une douleur thoracique intense

🚨 PharmaBot : ⚠️ URGENCE MÉDICALE
Les symptômes que vous décrivez nécessitent une consultation IMMÉDIATE.
Veuillez contacter le SAMU (15) ou vous rendre aux urgences.
on a fini. As-tu d'autres questions ?
```

### Cas 3 : Conversation suivie
```
👤 : J'ai de la fièvre
💊 : [Réponse 1]
👤 : Et des courbatures
💊 : [Réponse contextuelle sans répéter]
```

---

## ⚙️ Développement

### Tests
```bash
# Tester les fonctions utilitaires
python -c "from utils import check_grave_symptoms; print(check_grave_symptoms('douleur thoracique'))"

# Tester le prompt
python -c "from prompts import get_pharma_prompt; print(get_pharma_prompt()[:200])"
```

### Logs
Les logs sont disponibles avec différents niveaux :
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # Pour le développement
```

### Extensions possibles
1. **Base de données** : Stockage persistant des conversations
2. **Multi-utilisateurs** : Sessions séparées
3. **Téléchargement PDF** : Export des conversations
4. **Notifications** : Rappels de suivi
5. **Multi-langues** : Support d'autres langues

---

## 🚨 Limitations et Sécurité

### Ce que PharmaBot FAIT
- ✅ Fournit des informations générales sur les symptômes
- ✅ Oriente vers les bonnes ressources médicales
- ✅ Donne des conseils pratiques non-médicaux
- ✅ Alerte en cas de symptômes graves

### Ce que PharmaBot NE FAIT PAS
- ❌ Établir des diagnostics médicaux
- ❌ Prescrire des médicaments
- ❌ Remplacer un professionnel de santé
- ❌ Donner des avis médicaux personnalisés

**⚠️ Important** : PharmaBot est un outil d'orientation. Consultez toujours un professionnel de santé pour tout problème médical.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. **Créez une branche** (`git checkout -b feature/AmazingFeature`)
3. **Commitez** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Poussez** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez une Pull Request**

### Standards de code
- Respectez le style PEP 8
- Ajoutez des tests pour les nouvelles fonctionnalités
- Documentez votre code
- Mettez à jour le README si nécessaire

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

**Robert Kule**
- GitHub: [@RobertKule](https://github.com/RobertKule)
- Email: [kulewakangitsirobert@gmail.com](mailto:kulewakangitsirobert@gmail.com)

---

## 🙏 Remerciements

- **Google** pour l'API Gemini
- **LangChain** pour le framework d'IA
- **Streamlit** pour l'interface web
- Tous les contributeurs et testeurs

---

## 📞 Support

Pour toute question ou problème :
1. Consultez les [Issues](https://github.com/RobertKule/pharmabot/issues)
2. Ouvrez une nouvelle issue si nécessaire
3. Contactez l'auteur pour les questions urgentes

---

## ⭐ Soutien

Si ce projet vous est utile, n'hésitez pas à :
- ⭐ **Mettre une étoile** sur GitHub
- 🐛 **Signaler les bugs**
- 💡 **Proposer des améliorations**
- 🔄 **Partager** avec vos collègues

**PharmaBot** - L'orientation pharmaceutique intelligente et responsable.
```
