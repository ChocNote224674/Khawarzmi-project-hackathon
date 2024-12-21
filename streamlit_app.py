import requests
import streamlit as st
from typing import List

# URL de l'API (Assurez-vous que l'API est en cours d'exécution)
API_URL = "http://127.0.0.1:8000"

# Modèle de document pour affichage
class DocumentResponse:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata


# Interface Streamlit
st.title("Chatbot Documentaire")
st.markdown("Posez une question et obtenez une réponse basée sur vos documents locaux.")

# Entrées utilisateur
question = st.text_input("Votre question :", placeholder="Entrez votre question ici...")
temperature = st.slider("Température (Créativité)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
similarity_threshold = st.slider("Seuil de similarité", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

# Bouton pour récupérer les sources
if st.button("Récupérer les documents pertinents"):
    if not question:
        st.error("Veuillez entrer une question.")
    else:
        with st.spinner("Recherche des documents pertinents..."):
            response = requests.post(
                f"{API_URL}/get_sources",
                json={
                    "question": question,
                    "temperature": temperature,
                    "similarity_threshold": similarity_threshold,
                },
            )
            if response.status_code == 200:
                docs = response.json()
                if docs:
                    st.success(f"{len(docs)} documents trouvés.")
                    for i, doc in enumerate(docs, start=1):
                        st.markdown(f"### Document {i}")
                        st.write(f"**Contenu :** {doc['page_content'][:500]}...")
                        st.write(f"**Métadonnées :** {doc['metadata']}")
                else:
                    st.warning("Aucun document pertinent trouvé.")
            else:
                st.error(f"Erreur lors de la requête : {response.status_code}")

# Bouton pour obtenir une réponse
if st.button("Obtenir une réponse"):
    if not question:
        st.error("Veuillez entrer une question.")
    else:
        with st.spinner("Génération de la réponse..."):
            response = requests.post(
                f"{API_URL}/answer",
                json={
                    "question": question,
                    "temperature": temperature,
                    "similarity_threshold": similarity_threshold,
                },
            )
            if response.status_code == 200:
                data = response.json()
                st.success("Réponse générée :")
                st.markdown(f"### Réponse :\n{data['message']}")
                if data.get("documents"):
                    st.markdown("### Documents Utilisés :")
                    for i, doc in enumerate(data["documents"], start=1):
                        st.write(f"**Document {i} :** {doc[:500]}...")
            else:
                st.error(f"Erreur lors de la requête : {response.status_code}")
