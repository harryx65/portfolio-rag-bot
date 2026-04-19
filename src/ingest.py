from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

DATA_FOLDER = Path("data")
CHROMA_FOLDER = "storage/chroma"

# load markdown files


def load_markdown_files():
    documents = []

    for file_path in DATA_FOLDER.rglob("*.md"):
        loader = TextLoader(str(file_path), encoding="utf-8")
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = str(file_path)

        documents.extend(docs)

    return documents


# Split documents into chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


def main():
    print("Loading markdown files...")
    documents = load_markdown_files()
    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings and saving to ChromaDB...")
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_FOLDER
    )

    print("Ingestion complete!")
    print(f"Chroma database saved in: {CHROMA_FOLDER}")


if __name__ == "__main__":
    main()
