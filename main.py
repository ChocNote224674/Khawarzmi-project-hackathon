import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.document_loader import load_documents, preprocess_documents
from utils.embeddings import create_vector_store, search_relevant_docs
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

load_dotenv()

# Clé OpenAI depuis .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("La clé OpenAI n'est pas définie dans le fichier .env")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

app = FastAPI()

# Charger les documents et créer un magasin vectoriel (vector store)
DOCUMENT_FOLDER = "DATA"
documents = load_documents(DOCUMENT_FOLDER)
processed_docs = preprocess_documents(documents)
vector_store = create_vector_store(processed_docs)


class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict


class UserInput(BaseModel):
    question: str
    temperature: float = 0.7
    similarity_threshold: float = 0.5


@app.post("/get_sources", response_model=List[DocumentResponse])
def get_sources(user_input: UserInput) -> List[DocumentResponse]:
    """
    Récupérer les documents pertinents en fonction de la requête.
    """
    relevant_docs = search_relevant_docs(
        user_input.question, vector_store, similarity_threshold=user_input.similarity_threshold
    )

    if not relevant_docs:
        return []

    return [
        DocumentResponse(page_content=doc.page_content, metadata=doc.metadata)
        for doc in relevant_docs
    ]


@app.post("/answer")
def answer(user_input: UserInput):
    """
    Générer une réponse à partir des documents et de la question.
    """
    relevant_docs = search_relevant_docs(
        user_input.question, vector_store, similarity_threshold=user_input.similarity_threshold
    )

    if not relevant_docs:
        return {"message": "Aucun document pertinent trouvé pour répondre à la question."}

    chain = load_qa_chain(OpenAI(temperature=user_input.temperature), chain_type="stuff")
    answer = chain.run(input_documents=relevant_docs, question=user_input.question)

    return {"message": answer, "documents": [doc.page_content for doc in relevant_docs]}
