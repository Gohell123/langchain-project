from langchain_ollama import ChatOllama
from config import GEMINI_API_KEY

def get_llm():
    return ChatOllama(
        model="qwen3:1.7b")