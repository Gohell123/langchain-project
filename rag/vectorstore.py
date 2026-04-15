from langchain_pinecone import PineconeVectorStore
from config import INDEX_NAME
from rag.embeddings import get_embeddings

def get_vectorstore():
    return PineconeVectorStore(
        embedding=get_embeddings(),
        index_name=INDEX_NAME
    )