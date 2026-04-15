from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from llm.model import get_llm

from tools.search import search
from tools.rag import retrieve_context
from tools.business import get_product_price, get_product_discount

def load_prompt():
    with open("prompts/system_prompts.txt") as f:
        return f.read()

def build_agent():
    llm = get_llm()

    tools = [
        get_product_price,
        get_product_discount,
        retrieve_context,
        search
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
    )

    system_prompt = load_prompt()

    return agent, llm, system_prompt

