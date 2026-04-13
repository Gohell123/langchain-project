from operator import itemgetter
import os

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

print("Initializing..")


embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm=ChatOllama(model="qwen3:1.7b")
vectorstore=PineconeVectorStore(embedding=embeddings,index_name=os.environ['INDEX_NAME'])

retriever=vectorstore.as_retriever(search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.8,"k":3})

prompt_template=ChatPromptTemplate.from_template(
    """Answer the question based only on below context:
    {context}
    Question:{question}

    Provide a detailed answer""")

def format_docs(docs):
    """Format retrieved documents into single string"""
    return "\n\n".join(doc.page_content for doc in docs)

#Use Implementation without LCEL

def retrieval_chain_without_lcel(query:str):
    #Step1 : retrieve relevant documents
    docs=retriever.invoke(query)
    #Step2:Format documents into context string
    context=format_docs(docs)
    #Step3: Format the prompt with questiona and content
    messages=prompt_template.format_messages(context=context,question=query)
    #Step4 : Invoke the LLM with formatted Prompt
    response=llm.invoke(messages)

    return response.content


def retrieval_chain_with_lcel():
    """This function will return the langchain chain object that can be invoked with {"question":"..."}
    """
    retrieval_chain=(
        RunnablePassthrough.assign(
            context=itemgetter("question")|retriever|format_docs
            )
        | prompt_template
        | llm
        | StrOutputParser()    #StrOutputParser is used to get response.content
        )

    return retrieval_chain



if __name__=="__main__":
    print("Retrieving..")

    #Query
    query="What are Vector databases?"
    result_without_lcel=retrieval_chain_without_lcel(query)
    print("Result without lcel",result_without_lcel)

    result_with_lcel=retrieval_chain_with_lcel()
    final_answer=result_with_lcel.invoke({"question":query})

    print("Answer..")
    print(final_answer)




