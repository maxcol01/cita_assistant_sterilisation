import os
from dotenv import load_dotenv  

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
THAURA_AI_API_KEY = os.getenv("THAURA_AI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Configuration de l'environnement pour LangSmith
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY or ""
os.environ["LANGSMITH_PROJECT"] = "assistant-sterilisation"
os.environ["OPENAI_API_KEY"] = OPEN_AI_API_KEY or ""

