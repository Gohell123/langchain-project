from dotenv import load_dotenv
load_dotenv()
from agent.agent import build_agent
from langchain_core.messages import HumanMessage, SystemMessage
import os
from tools.search import search
from tools.rag import retrieve_context
from tools.business import get_product_price, get_product_discount
import time

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

def summarize_search(llm, raw_text):
    prompt=f"""You are a helpful assistant. 
    Summarize the text nicely that is easy to read.
    Remove Hyperlinks ,ads, irrelevant context.
    
    Content:{raw_text}
    """
    

    response=llm.invoke([
        SystemMessage(content=prompt)])

    return response.content

def needs_summarization(text):
    return len(text) > 1200 or "http" in text.lower()



def route_query(query: str,chat_history) -> str:
    query = query.lower()

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

    # Default → search
    return "search"

def trim_text(text, max_chars=1200):
    return text[:max_chars]



def main():
    
    print("HI, I am your Assistant. How may I help you today?")
    agent, llm, system_prompt = build_agent()

    while True:
        query = input("Ask something: (type 'exit' to quit): ") 
        
        if query.lower() == "exit":
            break
        start=time.time()

        route = route_query(query,chat_history)

        if route == "search":
            print("\n[ROUTER] Using Search directly...\n")
            result = search.invoke({"query": query})
            result = str(result) if result else ""

            #Making LLM call to summarize the result nicely
            if result and result.strip():
                if needs_summarization(result):
                    clean_answer = summarize_search(llm, trim_text(result))
                    print(clean_answer)
                else:
                    print(result)
            else:
                print("No results found. Falling back to agent...\n")
                route = "agent"
                            

        elif route == "rag":
            print("\n[ROUTER] Using RAG directly...\n")
            result = retrieve_context.invoke({"query": query})
            print("\n   Relevant Information:\n")
            print(result)

        else:
            print("\n[ROUTER] Using Agent...\n")
            # Add user message to history
            chat_history.append(HumanMessage(content=query))

            result = agent.invoke({
                "messages": [SystemMessage(content=system_prompt)]+chat_history
                })

            ai_message=result["messages"][-1]

            # Add AI response to history
            chat_history.append(ai_message)

            MAX_HISTORY = 6
            if len(chat_history) > MAX_HISTORY:
                chat_history[:] = chat_history[-MAX_HISTORY:]

            print("\n   Final Answer:\n")
            print(ai_message.content)
        
        end=time.time()
        print(f"Response Time: {round(end-start,2)} seconds")

if __name__ == "__main__":
    chat_history = []
    main()