import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Debug-Ausgabe ein-/ausschalten
# Aktiviert wird sie, wenn die Umgebungsvariable DEBUG auf
# "1", "true" oder "yes" gesetzt ist.
DEBUG = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")
