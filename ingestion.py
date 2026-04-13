import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
load_dotenv()

def main():
    print("Hello from langchain-project!")
    print(os.environ['PINECONE_API_KEY'])


if __name__ == "__main__":
    print("Ingesting..")
    file_path=r"C:\Users\lenovo\Documents\langchain\langchain-project\medium-vector-db-analyzer.txt"
    loader=TextLoader(file_path,autodetect_encoding=True)
    document=loader.load()
    
    print("Splitting")
    text_splitter=CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    chunks=text_splitter.split_documents(documents=document)
    print(f"Created Chunks:{len(chunks)}")


    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("ingesting..")
    PineconeVectorStore.from_documents(chunks,embeddings,index_name=os.environ['INDEX_NAME'])
    print("finish")




