conversation_summary=""
def summarize_text(llm,text:str) -> str:
    old_msg="/n".join([m.content for m in text])

    prompt = f"""Summarize the conversation briefly.
    keep the key facts, decisions and intent intact.
    Content :{old_msg} 
""" 
    response=llm.invoke([SystemMessage(content=prompt)])
    return response.content


conversation_summary=summarize_text(llm,old_messages)

messages=[SystemMessage(content=system_prompt),SystemMessage(content=f"{conversation_summary}")]+recent_history


embedding

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_vectorstore():
    return PineconeVectorStore(
        embedding=get_embeddings(),
        index_name=INDEX_NAME
    )

def get_retriever():
    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold":0.8, "k":3}
    )

@tool
def retrieve_context(query: str) -> str:
    """Always use this Tool if user asks about Vector databases.
    Retrieve relevant knowledge from vector DB"""
    retriever = get_retriever()
    docs = retriever.invoke(query)
    result=format_docs(docs)
    return result if result else "No relevant context found"


@tool
def retrieve_context(query:str) ->str:
    retriever=get_retriever()
    docs=retriever.invoke(query)
result=format(docs)


def format_docs(docs):
    return "\n".join[doc.page_content for doc in docs]


if any(x in query for x in ['price','cost'])