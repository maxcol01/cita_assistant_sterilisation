import streamlit as st
import pandas as pd
from assistant import get_rag_chain, add_documents_to_vector_db
from pathlib import Path
import os

st.set_page_config(page_title="Assistant de Knowledge Management", layout="wide")

st.title("Assistant de Knowledge Management:")
st.header("Service de stérilisation CHC Citadelle Liège")

# Initialisation de la chaîne RAG
if "rag_chain" not in st.session_state:
    st.session_state["rag_chain"] = get_rag_chain()

# Gestion de l'historique du chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Affichage des messages existants
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Entrez votre question ici, je me ferai un plaisir de vous répondre."):
    # Ajouter le message utilisateur à l'historique
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer la réponse
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # On utilise invoke pour la simplicité, ou stream pour l'effet temps réel
        try:
            response = st.session_state["rag_chain"].invoke(prompt)
            full_response = response
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Erreur lors de la génération de la réponse : {e}")
            full_response = "Désolé, une erreur est survenue."
            message_placeholder.markdown(full_response)
            
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# Sidebar pour la gestion des documents
with st.sidebar:
    st.title("Documents")
    path = Path("./documents/documents_list.csv")
    if path.exists():
        df = pd.read_csv(path, header=0)
        st.dataframe(df)
    else:
        st.error("Liste des documents introuvable.")


