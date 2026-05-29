

import tempfile
import streamlit as st
import google.generativeai as genai

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS



GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


@st.cache_resource
def load_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embeddings = load_embeddings()



@st.cache_resource
def create_vector_db(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    filtered_docs = []

    for doc in documents:

        text = doc.page_content.lower()

        if (
            "table of contents" in text
            or "contents" in text[:500]
            or "index" in text[:300]
        ):
            continue

        filtered_docs.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250
    )

    docs = text_splitter.split_documents(
        filtered_docs
    )

    vector_db = FAISS.from_documents(
        docs,
        embeddings
    )

    return vector_db


def ask_financial_question(question, vector_db):

    retrieved_docs = vector_db.similarity_search(
        question,
        k=6
    )

    context = "\n\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    prompt = f"""
    You are a senior financial analyst.

    Answer only from the provided report context.

    If information is not available in the report,
    respond with:

    Information not found in the report.

    Provide:

    1. Direct Answer
    2. Detailed Explanation
    3. Key Financial Insights

    Context:
    {context}

    Question:
    {question}
    """

    response = model.generate_content(
        prompt
    )

    return response.text, retrieved_docs



st.set_page_config(
    page_title="Financial Report RAG Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Report RAG Assistant")

uploaded_file = st.file_uploader(
    "Upload Annual Report PDF",
    type=["pdf"]
)

if uploaded_file:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(
            uploaded_file.read()
        )

        pdf_path = tmp_file.name

    with st.spinner(
        "Processing Financial Report..."
    ):

        vector_db = create_vector_db(
            pdf_path
        )

    st.success(
        "PDF Processed Successfully"
    )

    question = st.text_input(
        "Ask a question about the report"
    )

    col1, col2 = st.columns(2)

    ask_button = col1.button(
        "Get Answer"
    )

    summary_button = col2.button(
        "Generate Executive Summary"
    )


    if ask_button:

        if question:

            with st.spinner(
                "Generating Answer..."
            ):

                answer, sources = ask_financial_question(
                    question,
                    vector_db
                )

            st.subheader(
                "Answer"
            )

            st.write(
                answer
            )

            st.subheader(
                "Source Citations"
            )

            for i, doc in enumerate(
                sources
            ):

                with st.expander(
                    f"Source {i+1}"
                ):

                    st.write(
                        doc.page_content[:1200]
                    )

    

    if summary_button:

        with st.spinner(
            "Generating Executive Summary..."
        ):

            docs = vector_db.similarity_search(
                "financial performance revenue profit risk management business strategy future outlook",
                k=20
        )

            summary_context = "\n\n".join(
                [doc.page_content for doc in docs]
            )

            summary_prompt = f"""
            Create a professional executive summary of this annual report.

            Include:

            1. Business Overview
            2. Revenue Performance
            3. Profitability Analysis
            4. Key Risks
            5. Growth Opportunities
            6. Future Outlook

            Context:

            {summary_context}
            """

            summary = model.generate_content(
                summary_prompt
            )

            st.subheader(
                "Executive Summary"
            )

            st.write(
                summary.text
            )

