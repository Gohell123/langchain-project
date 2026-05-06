import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
    text_splitter=CharacterTextSplitter(chunk_size=800,chunk_overlap=100)
    chunks=text_splitter.split_documents(documents=document)
    print(f"Created Chunks:{len(chunks)}")


    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

    print("ingesting..")
    PineconeVectorStore.from_documents(chunks,embeddings,index_name=os.environ['INDEX_NAME'])
    print("finish")




