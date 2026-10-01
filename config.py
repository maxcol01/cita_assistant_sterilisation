import os
from dotenv import load_dotenv

# ============================================================
# Configuration de l'environnement
# ============================================================
# Ce module centralise la lecture des variables d'environnement
# depuis le fichier .env et configure les paramètres globaux :
#   1. Chargement du fichier .env (clés API)
#   2. Clés nécessaires : OpenAI, Thaura AI, LangSmith (optionnel)
#   3. Activation du tracing LangSmith pour le monitoring
#      des chaînes RAG (endpoint, projet, clé)
#   4. Export des variables dans os.environ pour que les
#      bibliothèques (LangChain, OpenAI SDK) les retrouvent
# ============================================================
  

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
THAURA_AI_API_KEY = os.getenv("THAURA_AI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# TODO: N'activer LANGSMITH_TRACING que si LANGSMITH_API_KEY est présente (éviter les warnings inutiles)
# Configuration de l'environnement pour LangSmith
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY or ""
os.environ["LANGSMITH_PROJECT"] = "assistant-sterilisation"
os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY or ""

