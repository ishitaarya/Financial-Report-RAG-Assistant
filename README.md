#  Financial Report RAG Assistant

An AI-powered Financial Report RAG Assistant that enables users to upload annual reports, perform semantic search using FAISS, and generate context-aware answers, financial insights, and executive summaries using Google Gemini.

##  Features
- PDF Upload & Processing
- Semantic Search with FAISS
- Financial Question Answering
- Executive Summary Generation
- Source Citations
- Gemini-Powered Insights

##  Tech Stack
Python | Streamlit | LangChain | FAISS | Gemini API | HuggingFace Embeddings | PyPDF

## Workflow
PDF → Chunking → Embeddings → FAISS → Retriever → Gemini → Answer

##  Run Locally

pip install -r requirements.txt
streamlit run app.py


