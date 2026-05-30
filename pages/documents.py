import streamlit as st
from pathlib import Path
import pandas as pd
from typing import Optional
from datetime import datetime
from assistant import add_document_to_vector_db
# Constantes
DOC_PATH = Path(__file__).parent.parent / "documents"
DB_FILE = DOC_PATH / "documents_list.csv"

# Fonctions

def add_document_to_db(names: list, path: Path) -> None:
    list_files = []
    for file_name in names:
        row = {"name": file_name, "location": path / f"{file_name}", "date":datetime.today().date()}
        list_files.append(row)
    df = pd.DataFrame(list_files)

    # if we indeed selected some file to add:
    if len(df) != 0:
        try:
            db = pd.read_csv(DB_FILE, header=0)
        except FileNotFoundError:
            df.to_csv(DB_FILE, index=False)
            st.session_state["is_saved"] = "Document(s) ajouté(s) avec succès dans vote base de connaissance !"
        else:
            documents_to_look_for = "|".join(names)
            print(documents_to_look_for)
            duplicate = db.name.str.contains(documents_to_look_for)
            print(duplicate)
            db_full = pd.concat([db, df], axis=0)
            db_full = db_full.drop_duplicates(subset=["name"])
            db_full.to_csv(DB_FILE, index=False)
            st.session_state["is_saved"] = "Document(s) ajouté(s) avec succès dans vote base de connaissance !"
            if any(duplicate):
                st.session_state["warning"] = "Certains fichier(s) déjà présents dans la base de données nous pas été ajoutés à nouveau!"
    return DB_FILE

# Session state 
if "show_uploader" not in st.session_state:
    st.session_state["show_uploader"] = False


if "warning" in st.session_state:
    st.warning(st.session_state.pop("warning"))


if "is_saved" in st.session_state:
    st.success(st.session_state.pop("is_saved"))


# Corps de page

st.header("Liste des documents disponibles pour la consultation de l'assistant")
st.text("Voci la liste des documents actuellement dans votre base de données consultable par l'assistant IA. Pour ajouter des documents, sélectionner le bouton dédé ci-dessous. Ce(s) document(s) sera(seront) automatiquement ajouté(s) à vos sources consultables.")


try:
    db = pd.read_csv(DB_FILE, header=0)
except FileNotFoundError:
    st.write("Aucun documents disponibles")
else:
    st.dataframe(db[["name","date"]])

if st.button("Ajouter un document"):
    st.session_state["show_uploader"] = True

if st.session_state["show_uploader"]:
    uploaded_file: Optional[pd.DataFrame] = st.file_uploader(label="Uploader votre document", accept_multiple_files=True)
    
    if uploaded_file:
        names = [file_.name for file_ in uploaded_file]
        db_path = add_document_to_db(names, DOC_PATH)
        add_document_to_vector_db(db_path)
        st.session_state["show_uploader"] = False
        st.rerun()