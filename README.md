# 🚛 FleetMind AI

**AI-Powered Heavy Equipment Maintenance Assistant**

FleetMind AI is a Retrieval-Augmented Generation (RAG) chatbot that lets maintenance engineers query heavy-duty truck manuals using natural language. Ask any maintenance question and get precise, source-cited answers instantly.

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-green)](https://www.trychroma.com)
[![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev)

---

## ✨ Features

- 🔍 **Semantic Search** — Find answers across hundreds of pages using vector similarity, not keywords
- 🤖 **Gemini-Powered Answers** — Context-grounded responses using Google's Gemini LLM
- 📂 **Upload Documents** — Add new PDF manuals at runtime; they are instantly indexed and searchable
- 🗄 **ChromaDB Vector Store** — Persistent, fast similarity search with 3795+ indexed chunks
- 📄 **Source Citations** — Every answer shows the exact manual and page it came from
- 📊 **Live Stats** — Sidebar shows real-time knowledge base metrics

---

## 🏗 Architecture

```
User Question
     │
     ▼
Sentence Transformer (all-MiniLM-L6-v2)
     │  embed query
     ▼
ChromaDB Vector Store
     │  top-5 relevant chunks
     ▼
Google Gemini (gemini-3.5-flash)
     │  context-grounded generation
     ▼
Answer + Source Citations
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| PDF Parsing | PyMuPDF (fitz) |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Embeddings | `all-MiniLM-L6-v2` (Sentence Transformers) |
| Vector Database | ChromaDB (persistent) |
| LLM | Google Gemini via `google-genai` |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
FleetMind_AI/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── packages.txt                # Linux system packages (for cloud)
├── .env                        # Local API key (never commit)
│
├── src/
│   ├── pdf_loader.py           # PDF → page text extraction
│   ├── chunker.py              # Text → overlapping chunks
│   ├── embedding_generator.py  # Chunks → embedding vectors
│   ├── vector_store.py         # ChromaDB storage (store + append)
│   ├── retriever.py            # Semantic search queries
│   ├── llm.py                  # Gemini answer generation
│   └── uploader.py             # Runtime PDF upload pipeline
│
├── components/
│   ├── hero.py                 # Hero section UI
│   ├── answer_card.py          # Answer display card
│   ├── source_cards.py         # Source citation cards
│   └── upload_panel.py         # Sidebar upload widget
│
├── data/manuals/               # Source PDF manuals
├── chroma_db/                  # Persistent vector database
└── assets/style.css            # Custom CSS styling
```

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/FleetMind_AI.git
cd FleetMind_AI
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Google API key
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your-api-key-here
```
Get your key at [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Index your manuals (first time only)
Place PDF files in `data/manuals/`, then run:
```bash
cd src
python index_documents.py
```

### 6. Run the app
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/FleetMind_AI.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **"New app"**
3. Select your repository and set **Main file path** to `app.py`
4. Click **"Advanced settings"** → **Secrets** and add:
   ```toml
   GOOGLE_API_KEY = "your-api-key-here"
   ```
5. Click **Deploy** ✅

> The `chroma_db/` folder is included in the repo — your 3 pre-indexed manuals are available immediately without re-indexing.

---

## 📖 Usage

### Ask a question
Type any maintenance question in the chat input:
> *"What is the oil change interval for a Volvo FH16?"*
> *"How do I bleed the brake system on a Mack Titan?"*

### Upload a new manual
1. Open the **sidebar** → **📂 Upload Documents**
2. Drag & drop one or more PDF files
3. Click **⚡ Index Documents**
4. The new manual is searchable immediately

---

## ⚙️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | ✅ Yes |

---

Feel free to use and adapt this project.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io) — rapid app framework
- [ChromaDB](https://www.trychroma.com) — vector database
- [Sentence Transformers](https://www.sbert.net) — embedding model
- [Google Gemini](https://ai.google.dev) — large language model
- [LangChain](https://langchain.com) — text splitting utilities
- [PyMuPDF](https://pymupdf.readthedocs.io) — PDF parsing
