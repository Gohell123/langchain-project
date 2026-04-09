import os
from dotenv import load_dotenv
load_dotenv()
print("API KEY:", os.getenv("GEMINI_API_KEY"))

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient



print("Tracing:", os.getenv("LANGSMITH_TRACING"))
print("API Key:", os.getenv("LANGSMITH_API_KEY"))
print("Project:", os.getenv("LANGSMITH_PROJECT"))

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search(query:str) -> str:
    """
    Tool that searches the web for the given query
    Args:
    query: The search query
    Returns:
    The search results
    """
    print(f"Searching for: {query}")
    return tavily.search(query=query)

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0)

print(llm.model)
tools=[search]
agent=create_agent(model=llm,tools=tools)


def main():
    print("Hello from langchain-project!")

    result=agent.invoke(
        {'messages':[HumanMessage(content="Search 3 Job Postings for AI Engineer requiring experience in between 7-11 years in Pune location on Naukri Portal and summarize the results in 3 lines.")]},
    )
    print(result)

if __name__ == "__main__":
    main()
