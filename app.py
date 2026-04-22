from dotenv import load_dotenv
load_dotenv()
from agent.agent import build_agent
from langchain_core.messages import HumanMessage, SystemMessage
import os
from tools.search import search
from tools.rag import retrieve_context
from tools.business import get_product_price, get_product_discount
from cache.cache import get_cache,set_cache,add_semantic_cache,get_semantic_cache
import time

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

def summarize_search(llm, raw_text):
    prompt=f"""You are a helpful assistant. 
    Summarize the text nicely that is easy to read.
    Remove Hyperlinks ,ads, irrelevant context.
    """
    

    response=llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=raw_text)])

    return response.content

def needs_summarization(text):
    return len(text) > 2000 or "http" in text.lower()


def is_small_talk(query:str) -> bool:
    query=query.lower()
    greet_chat = [
        "hi", "hello", "hey",
        "how are you", "how are you doing",
        "what's up", "wassup",
        "how's it going",
        "good morning", "good evening",
        "bye", "take care"
    ]
    return any(x in query for x in greet_chat)


def vague_queries(query:str) -> bool:
    bad_patterns=['non-sense','stupid','dumb','shut up','never bother']
    return any(x in query for x in bad_patterns) or len(query)<3




def route_query(query: str,chat_history) -> str:
    query = query.lower()

    if is_small_talk(query):
        return "chat"
    

    if chat_history:
        last_user = ""
        for msg in reversed(chat_history):
            if isinstance(msg, HumanMessage):
                last_user = msg.content.lower()
                break
        
        if any(x in query for x in ["apply", "it", "that", "this", "tier"]):
            return "agent"
  

    # Business logic
    if any(x in query for x in ["price", "cost", "discount"]):
        return "agent"

    # Internal knowledge (RAG)
    if any(x in query for x in ["vector", "embedding", "rag", "internal"]):
        return "rag"
    
    if any(x in query for x in ["latest","recent","top","best","news"]):
        return "search"

    # Default → search
    return "agent"

def trim_text(text, max_chars=1200):
    return text[:max_chars]



def handle_query(query, agent, llm, system_prompt, chat_history):
    route = route_query(query, chat_history)

    # ---------------- SEARCH ----------------
    if route == "search":
        cached = get_cache(query)
        if cached:
            return cached

        semantic = get_semantic_cache(query)
        if semantic:
            return semantic

        try:
            result = search.invoke({"query": query})
            result = str(result) if result else ""

            if needs_summarization(result):
                answer = summarize_search(llm, trim_text(result))
            else:
                answer = result

            set_cache(query, answer)
            add_semantic_cache(query, answer)

            return answer

        except Exception:
            route = "agent"   # fallback

    # ---------------- RAG ----------------
    if route == "rag":
        cached = get_cache(query)
        if cached:
            return cached

        semantic = get_semantic_cache(query)
        if semantic:
            return semantic

        try:
            result = retrieve_context.invoke({"query": query})

            if not result:
                raise ValueError("Empty RAG result")

            answer = str(result)

            set_cache(query, answer)
            add_semantic_cache(query, answer)

            return answer

        except Exception:
            route = "agent"

    # ---------------- CHAT ----------------
    if route == "chat":
        cached = get_cache(query)
        if cached:
            return cached

        semantic = get_semantic_cache(query)
        if semantic:
            return semantic

        response = llm.invoke([
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=query)
        ])

        answer = response.content

        set_cache(query, answer)
        add_semantic_cache(query, answer)

        return answer

    # ---------------- AGENT ----------------
    if route == "agent":
        cached = get_cache(query)
        if cached:
            return cached

        semantic = get_semantic_cache(query)
        if semantic:
            return semantic
        

        try:
            chat_history.append(HumanMessage(content=query))

            result = agent.invoke({
                "messages": [SystemMessage(content=system_prompt)] + chat_history
            })

            ai_message = result["messages"][-1]
            answer = ai_message.content or "No response generated."

            chat_history.append(ai_message)

            # Limit memory
            MAX_HISTORY = 6
            if len(chat_history) > MAX_HISTORY:
                chat_history[:] = chat_history[-MAX_HISTORY:]

            set_cache(query, answer)
            add_semantic_cache(query, answer)

            return answer

        except Exception as e:
            print(e)
            return "Something went wrong. Please try again."

def main():
    chat_history=[]
    print("Hi, I am your Assistant. How may I help you today?")
    agent, llm, system_prompt = build_agent()
    while True:
        
        query = input("Ask something: (type 'exit' to quit): ")
        query = query.lower().strip()

        if query == "exit":
            break

        start = time.time()
        if vague_queries(query):
             print("I'm here to help. Please let me know what you need.")
             continue

        answer = handle_query(query, agent, llm, system_prompt, chat_history)

        print("\nResponse:\n")
        print(answer)

        end = time.time()
        print(f"Response Time: {round(end-start,2)} seconds")


if __name__=='__main__':
    main()
    