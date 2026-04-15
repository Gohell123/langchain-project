from rag.vectorstore import get_vectorstore

def get_retriever():
    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold":0.8, "k":3}
    )