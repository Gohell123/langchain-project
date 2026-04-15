from langchain.tools import tool
from rag.retriever import get_retriever
from langsmith import traceable



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@tool
def retrieve_context(query: str) -> str:
    """Retrieve relevant knowledge from vector DB"""
    retriever = get_retriever()
    docs = retriever.invoke(query)
    result=format_docs(docs)
    return result if result else "No relevant context found"