import streamlit as st
import pandas as pd

st.title("Assistant de Knowledge Management:")
st.header("Service de stérilisation CHC Citadelle Liége")

if "question" not in st.session_state:
    st.session_state["question"] = "" 


question = st.chat_input(placeholder="Entrez votre question ici, je me ferai un plaisir de vous répondre.")

if question == None:
    question = ""

st.session_state["question"] += str(question) + "\n\n"


with st.chat_message("user"):
    st.write(f"{st.session_state["question"]}")

with st.chat_message("ai"):
    st.write("Fine")

path = "./documents/documents_list.csv"

df = pd.read_csv(path, header=0)

st.dataframe(df)