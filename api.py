from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

import os

# -----------------------------
# Load env
# -----------------------------
load_dotenv()

CHROMA_FOLDER = "storage/chroma"

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(title="Portfolio RAG API")


# -----------------------------
# Request model (input)
# -----------------------------
class ChatRequest(BaseModel):
    question: str


# -----------------------------
# Load RAG system once
# -----------------------------
def load_rag_system():
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_FOLDER,
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llmm = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-120b",
        task='text-generation',
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
    )

    llm = ChatHuggingFace(llm=llmm)

    return retriever, llm


retriever, llm = load_rag_system()


# -----------------------------
# Test route
# -----------------------------
@app.get("/")
def home():
    return {"message": "API is running 🚀"}


# -----------------------------
# Chat endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question

    # Retrieve docs
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Clean sources
    sources = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown source")
        file_name = source.split("/")[-1].split("\\")[-1]
        if file_name not in sources:
            sources.append(file_name)

    # Prompt
    prompt = f"""
You are a portfolio chatbot for Muhammad Haris.

Answer ONLY using the context below.

If the question asks for a list, extract all items clearly.

If the answer is not found, say:
"I couldn't find that information in my portfolio data."

Keep the answer clear, natural, and professional.

Context:
{context}

Question:
{question}
"""

    # Get response
    response = llm.invoke(prompt)
    answer = response.content

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
