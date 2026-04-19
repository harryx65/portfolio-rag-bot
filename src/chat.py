from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os

load_dotenv()

CHROMA_FOLDER = "storage/chroma"


def main():
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',)

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

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are an AI portfolio assistant for Muhammad Haris.

Your job is to answer questions only from the provided context.

Rules:
1. Use only the information from the context.
2. Do not make up any details.
3. If the answer is not in the context, say:
   "I couldn't find that information in my portfolio data."
4. Keep answers clear, natural, and professional.
5. If the question is about skills, projects, or experience, answer in short bullet points when helpful.
6. If possible, mention the most relevant project or skill directly.
7. Keep the answer concise unless the question asks for detail.

Context:
{context}

Question:
{question}


"""

        response = llm.invoke(prompt)

        print("\nBot:", response.content)

        # Step 11: Print sources
        # print("\nSources:")
        # for doc in docs:
        #     print("-", doc.metadata.get("source", "Unknown source"))

        # print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
