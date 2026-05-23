import streamlit as st
from pathlib import Path
import pandas as pd
from typing import Optional

# Constantes
DOC_PATH = Path(__file__).parent.parent / "documents"
DB_FILE = DOC_PATH / "documents_list.csv"

# Fonctions

def add_document_to_db(file_name: str, path: Path) -> None:
    row = {"name": file_name, "location": path / f"{file_name}"}
    df = pd.DataFrame([row])
    
    try:
        db = pd.read_csv(DB_FILE, header=0)
    except FileNotFoundError:
        df.to_csv(DB_FILE, index=False)
        st.session_state["is_saved"] = "Document ajouté avec succès dans vote base de connaissance !"
    else:
        if not any(db.name.str.contains(file_name)):
            db_full = pd.concat([db, df], axis=0)
            db_full.to_csv(DB_FILE, index=False)
            st.session_state["is_saved"] = "Document ajouté avec succès dans vote base de connaissance !"
        else:
            st.session_state["warning"] = "Fichier déjà dans la base de données !"

# Session state 
if "show_uploader" not in st.session_state:
    st.session_state["show_uploader"] = False


if "warning" in st.session_state:
    st.warning(st.session_state.pop("warning"))


if "is_saved" in st.session_state:
    st.success(st.session_state.pop("is_saved"))


# Corps de page

st.header("Liste des documents disponibles pour la consultation de l'assistant")
st.text("Voci la liste des documents actuellement dans votre base de données consultable par l'assistant IA. Pour ajouter des documents, sélectionner le bouton dédé ci-dessous. Ce(s) document(s) sera(seront) automatiquement ajoutés à vos sources consultables.")


try:
    db = pd.read_csv(DB_FILE, header=0)
except FileNotFoundError:
    st.write("Aucun documents disponibles")
else:
    st.dataframe(db["name"])

if st.button("Ajouter un document"):
    st.session_state["show_uploader"] = True

if st.session_state["show_uploader"]:
    uploaded_file: Optional[pd.DataFrame] = st.file_uploader(label="Uploader votre document")
    
    if uploaded_file is not None:
        add_document_to_db(uploaded_file.name, DOC_PATH)
        st.session_state["show_uploader"] = False
        st.rerun()