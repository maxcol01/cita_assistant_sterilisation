# Assistant de Knowledge Management - Service de Stérilisation (CHC Citadelle)

Ce projet est un assistant intelligent basé sur l'IA (RAG - Retrieval-Augmented Generation) conçu pour aider le personnel du service de stérilisation du **CHC Citadelle à Liège**. Il permet d'interroger la documentation technique et les guides de bonnes pratiques via une interface de chat simple et intuitive.

## 🚀 Fonctionnalités

- **Chatbot Intelligent** : Posez des questions en langage naturel sur les procédures de stérilisation.
- **Réponses Sourcées** : Chaque réponse inclut les sources précises (nom du fichier et numéro de page) extraites des documents officiels.
- **Extraction Markdown** : Utilisation de `PyMuPDF4LLM` pour une extraction fidèle de la structure des documents (titres, listes, gras).
- **Base de Connaissance Dynamique** : Interface dédiée pour uploader de nouveaux PDF et les indexer instantanément dans la base vectorielle.
- **Recherche Sémantique** : Utilisation de `ChromaDB` et des embeddings OpenAI pour trouver l'information la plus pertinente, même si les mots exacts ne correspondent pas.

## 🛠️ Architecture Technique

- **Frontend** : [Streamlit](https://streamlit.io/)
- **Orchestration RAG** : [LangChain](https://www.langchain.com/)
- **LLM** : OpenAI `gpt-4o-mini`
- **Base Vectorielle** : [ChromaDB](https://www.trychroma.com/)
- **Traitement PDF** : [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF4LLM)
- **Observabilité** : Intégration optionnelle avec [LangSmith](https://www.langchain.com/langsmith) pour le monitoring des chaînes.

## 📂 Structure du Projet

- `app.py` : Point d'entrée de l'application Streamlit (Interface Chat).
- `assistant.py` : Logique métier du RAG (Indexation, Retrieval, Chaîne de réponse).
- `prompt.py` : Définition des instructions système pour l'IA.
- `config.py` : Gestion des variables d'environnement et configurations.
- `pages/` : Pages additionnelles de l'interface (Gestion des documents).
- `documents/` : Stockage des fichiers PDF et index CSV.
- `chroma_db/` : Base de données vectorielle persistante.

## ⚙️ Installation

1. **Cloner le repository** :
   ```bash
   git clone https://github.com/votre-compte/assistant-sterilisation.git
   cd assistant-sterilisation
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration** :
   Créez un fichier `.env` à la racine du projet avec vos clés API :
   ```env
   OPEN_AI_API_KEY=votre_cle_openai
   LANGSMITH_API_KEY=votre_cle_langsmith (optionnel)
   ```

## 📖 Utilisation

Lancez l'application avec Streamlit :
```bash
streamlit run app.py
```

1. Accédez à l'interface via votre navigateur (généralement `http://localhost:8501`).
2. Pour commencer, allez dans la section **Documents** (sidebar ou page dédiée) pour uploader vos PDF.
3. Cliquez sur **"Indexer les documents"** pour préparer la base de connaissance.
4. Posez vos questions dans le chat !

---
*Développé pour le CHC Citadelle - Service de Stérilisation.*
