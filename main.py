from dotenv import load_dotenv
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI  # <- NEU

# .env laden
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Chat-Modell initialisieren
chat = ChatOpenAI(api_key=api_key, temperature=0.7)

while True:
    user_input = input("Du: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = chat.invoke([HumanMessage(content=user_input)])  # <- NEU
    print("KI:", response.content)
