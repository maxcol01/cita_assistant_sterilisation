import streamlit as st
import pandas as pd
from assistant import get_rag_chain, add_documents_to_vector_db
from pathlib import Path
import os

# ============================================================
# Assistant de Knowledge Management - Service de Stérilisation
# CHC Citadelle Liège
# ============================================================
# Point d'entrée de l'application Streamlit.
# Ce script gère :
#   1. L'affichage du titre et de la configuration de page
#   2. L'initialisation de la chaîne RAG (via assistant.py)
#   3. La gestion de l'historique des messages du chat
#   4. L'envoi de la question à la chaîne RAG et l'affichage
#      de la réponse générée par le LLM
#   5. Une sidebar qui liste les documents indexés dans la base
#      vectorielle (lecture du CSV documents_list.csv)
# ============================================================

st.set_page_config(page_title="Assistant de Knowledge Management", layout="wide")

st.title("Assistant de Knowledge Management:")
st.header("Service de stérilisation CHC Citadelle Liège")

# TODO: Valider que THAURA_AI_API_KEY est présente avant d'initialiser la chaîne RAG
# Initialisation de la chaîne RAG
if "rag_chain" not in st.session_state:
    st.session_state["rag_chain"] = get_rag_chain()

# TODO: Historique persistant optionnel à ajouter (sauvegarde JSON locale entre sessions)
# Gestion de l'historique du chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Affichage des messages existants
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# TODO: Afficher 3-4 boutons de questions fréquentes sous le champ de saisie
# TODO: Afficher les sources en liens cliquables vers le PDF ouvert à la bonne page
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
        
        # TODO: Remplacer .invoke() par .stream() pour afficher la réponse en temps réel
        try:
            #TODO: Streaming de la réponse au lieu de .invoke()
            response = st.session_state["rag_chain"].invoke(prompt)
            full_response = response
            message_placeholder.markdown(full_response)
        except Exception as e:
            # TODO: Distinguer erreurs réseau (timeout, 500) et proposer un retry avec message propre
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
