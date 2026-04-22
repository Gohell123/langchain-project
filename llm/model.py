from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )