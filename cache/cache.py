from langchain_huggingface import HuggingFaceEmbeddings
import time
import numpy as np

# Exact cache with TTL
cache = {}

# Semantic cache
semantic_cache = []

# Embedding model
# embed_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

def set_cache(key,value):
    cache[key]=(value,time.time())


def get_cache(key,ttl=300):
    if key in cache:
        value,ts=cache[key]
        if time.time()-ts<ttl:
            return value
    return None


# def add_semantic_cache(query,response):
#     emb=embed_model.embed_query(query)
#     semantic_cache.append((emb,response,time.time()))


# def get_semantic_cache(query,threshold=0.85,ttl=300):
#     query_emb=embed_model.embed_query(query)

#     for emb,resp,ts in semantic_cache:
#         if time.time()-ts>ttl:
#             continue
#         sim=np.dot(query_emb,emb)/(np.linalg.norm(query_emb) * np.linalg.norm(emb))
#         if sim>threshold:
#             return resp
#     return None



                            