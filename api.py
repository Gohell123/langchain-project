from fastapi import FastAPI
from pydantic import BaseModel
from app import handle_query
from agent.agent import build_agent
import os
import redis
import json
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
#redis_client = redis.from_url(os.getenv("REDIS_URL"))

# 🔹 -------- Serialization helpers --------
def serialize_message(msg):
    # Skip ToolMessage completely
    if isinstance(msg, ToolMessage):
        return None

    return {
        "type": msg.__class__.__name__,
        "content": msg.content
    }


def deserialize_message(msg_dict):
    msg_type = msg_dict["type"]

    if msg_type == "HumanMessage":
        return HumanMessage(content=msg_dict["content"])

    elif msg_type == "AIMessage":
        return AIMessage(content=msg_dict["content"])



    return None


# -------- Redis helpers --------
def load_history(session_id):
    try:
        data = redis_client.get(session_id)
        if not data:
            return []

        messages = json.loads(data)

        return [
            deserialize_message(m)
            for m in messages
            if deserialize_message(m)
        ]

    except Exception as e:
        print("Redis load error:", e)
        redis_client.delete(session_id)
        return []


def save_history(session_id, chat_history):
    data = []

    for m in chat_history:
        serialized = serialize_message(m)
        if serialized:
            data.append(serialized)

    redis_client.set(session_id, json.dumps(data), ex=3600)




# Initialize app
app = FastAPI()

# Build agent once (important)
agent, llm, system_prompt = build_agent()

# In-memory chat storage (per session)
# memory_store = {}

# Request schema
class QueryRequest(BaseModel):
    query: str
    session_id: str


@app.get("/")
def home():
    return {"status":"running"}


@app.post("/chat")
def chat(request: QueryRequest):
    session_id = request.session_id
    query = request.query

    # Get or create chat history
    # if session_id not in memory_store:
    #     memory_store[session_id] = []

    # chat_history = memory_store[session_id]
    
    # Load chat history from Redis
    chat_history = load_history(session_id)

    # Call your existing logic
    try:
        answer = handle_query(query, agent, llm, system_prompt, chat_history)
    except Exception as e:
        print("Error",str(e))
        raise e

      # Save updated history back to Redis
    save_history(session_id, chat_history)

    return {
        "response": answer
    }