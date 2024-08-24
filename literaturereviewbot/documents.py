#!/usr/bin/env python3
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents.base import Document
from langchain_ollama import OllamaEmbeddings

# Create a vector store with a sample text
# from langchain_core.vectorstores import InMemoryVectorStore


def index_documents(query, abstract_arr, ids_arr: list | None = None):
    index = faiss.IndexFlatL2(
        len(OllamaEmbeddings(model="llama3.1").embed_query(query))
    )

    vector_store = FAISS(
        embedding_function=OllamaEmbeddings(model="llama3.1"),
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    docs = []
    for abstract in abstract_arr:
        # print(abstract)
        docs.append(Document(page_content=abstract))

    vector_store.add_documents(documents=docs, ids=ids_arr)

    return vector_store


def retrieve_documents(query, vector_store):
    # Use the vectorstore as a retriever
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
    )

    # Retrieve the most similar text
    return retriever.invoke(query)
