import os
from langchain.document_loaders import PyPDFLoader
def load_documents(folder_path: str):
    """
    Charger tous les fichiers PDF dans un dossier donné.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier {folder_path} n'existe pas.")

    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
    if not pdf_files:
        raise ValueError("Aucun fichier PDF trouvé dans le dossier.")

    documents = []
    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        documents.extend(loader.load())

    return documents


def preprocess_documents(documents):
    """
    Prétraiter les documents pour l'indexation.
    """
    for doc in documents:
        doc.metadata["source"] = doc.metadata.get("source", "local")
    return documents
