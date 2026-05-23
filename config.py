import os
from dotenv import load_dotenv  

load_dotenv()

api_key_openai = os.getenv("OPEN_AI_API_KEY")
langsmith_key = os.getenv("LANGSMITH_API_KEY")

