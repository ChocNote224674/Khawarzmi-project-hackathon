from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

def create_vector_store(documents):
    """
    Créer un magasin vectoriel (vector store) à partir des documents.
    """
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def search_relevant_docs(query, vector_store, similarity_threshold=0.5):
    """
    Rechercher des documents pertinents à l'aide du magasin vectoriel.
    """
    docs = vector_store.similarity_search(query, k=5)
    return [doc for doc in docs if doc.metadata.get("similarity", 1) >= similarity_threshold]

