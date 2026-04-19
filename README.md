# 🤖 Portfolio RAG Bot

An AI-powered portfolio chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer questions about Muhammad Haris — his skills, projects, education, and experience. Built with LangChain, ChromaDB, HuggingFace, FastAPI, and Streamlit.


## 📸 Demo

> Ask questions like:
> - *"What skills does Haris have?"*
> - *"List all his projects"*
> - *"Where did Haris study?"*
> - *"How can I contact Haris?"*


## 🧠 How It Works

1. **Ingest** — Markdown files (`about.md`, `education.md`, `experience.md`, `projects/`, `links.md`) are chunked and embedded into ChromaDB.
2. **Retrieve** — On each question, the top-3 most relevant chunks are retrieved from the vector store.
3. **Generate** — A HuggingFace-hosted LLM generates a grounded answer using only the retrieved context.



## 🗂️ Project Structure


portfolio_rag_bot/
├── data/                    # Portfolio content (Markdown files)
│   ├── about.md
│   ├── education.md
│   ├── experience.md
│   ├── links.md
│   └── projects/
├── src/
│   ├── ingest.py            # Ingest markdown → ChromaDB
│   └── chat.py              # (optional) CLI chat interface
├── storage/
│   └── chroma/              # Persisted vector store
├── api.py                   # FastAPI backend
├── api_streamlit.py         # Streamlit frontend
├── .env                     # Environment variables (not committed)
└── requirements.txt




## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/harryx65/portfolio-rag-bot.git
cd portfolio-rag-bot


### 2. Create and activate a virtual environment

```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
# macOS/Linux
source myenv/bin/activate


### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
HUGGINGFACEHUB_ACCESS_TOKEN=your_huggingface_token_here


### 5. Add your portfolio data

Edit the Markdown files inside the `data/` folder with your own content:

- `about.md` — Bio and summary
- `education.md` — Academic background
- `experience.md` — Work history
- `projects/` — One file per project (or a single combined file)
- `links.md` — Social and contact links

### 6. Ingest data into ChromaDB

```bash
python src/ingest.py
```

This will chunk your Markdown files and save embeddings to `storage/chroma/`.


## 🚀 Running the App

### Step 1 — Start the FastAPI backend

```bash
uvicorn api:app --reload
```

API will be live at: `http://127.0.0.1:8000`

You can test it at: `http://127.0.0.1:8000/docs`

### Step 2 — Start the Streamlit frontend

```bash
streamlit run api_streamlit.py

Frontend will open in your browser at: `http://localhost:8501`


## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | HuggingFace (`openai/gpt-oss-120b`) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| Orchestration | LangChain |
| Data Format | Markdown |


## 📬 Contact

**Muhammad Haris** — AI Engineer

- 📧 harisaslam.se@gmail.com
- 🔗 [LinkedIn](https://www.linkedin.com/in/muhammad-haris-14803022b/)
- 💼 [Upwork](https://www.upwork.com/freelancers/~01dcf054e52fdc82e0)
- 🎯 [Fiverr](https://www.fiverr.com/sellers/harisaslam242)
- 💻 [GitHub](https://github.com/harryx65)
