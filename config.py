# config.py
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé API depuis le fichier .env
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("La clé API OpenAI n'a pas été trouvée dans le fichier .env.")
