# app.py
import streamlit as st
import requests

API_URL_ASK = "http://127.0.0.1:8000/ask_questions/"
API_URL_REPORT = "http://127.0.0.1:8000/generate_report/"

# Initialiser l'état de la session pour l'historique des messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Could you propose a theme for a story?"}]

# Interface utilisateur Streamlit
st.title("Breast Cancer Monitoring Questions")

# Affichage des messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Demande d'entrée utilisateur
if user_input := st.chat_input("Ask a question:"):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Appel de l'API pour obtenir une réponse
    response = requests.post(API_URL_ASK, json={"questions": [user_input], "responses": {}})
    if response.status_code == 200:
        api_response = response.json()["responses"]
    else:
        api_response = "Error: Unable to process your request."

    # Ajouter la réponse de l'assistant à l'historique
    st.session_state["messages"].append({"role": "assistant", "content": api_response})

    # Appel de l'API pour générer un rapport médical une fois toutes les réponses collectées
    if user_input.lower() == "finish":
        report_response = requests.post(API_URL_REPORT, json={"responses": api_response})
        if report_response.status_code == 200:
            medical_report = report_response.json()["report"]
            st.write("Medical Report:", medical_report)
