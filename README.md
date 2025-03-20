# KobeRAG - Retrieval-Augmented Generation (RAG) Application

## Project Description
KobeRAG is a Retrieval-Augmented Generation (RAG) Web Application designed to:

- Upload and process **PDF** and **HTML** documents
- Perform **Hybrid Retrieval**: BM25 keyword search combined with Semantic Search
- Summarize answers using two modes:
  - **Ollama LLaMA 3 Local Model** (`main.py`)
  - **Hugging Face `facebook/bart-large-cnn` Free Summarizer** (`app.py`)
- Stream the answer **word-by-word** to the user
- Offer a clean **Bootstrap frontend** with **modal-based feedback**

The project fulfills the RAG requirements while offering flexibility between fully local and free cloud-enhanced summarization.

## Repository
**GitHub:** https://github.com/kobeoseijnr/KobeRAG

## Features
| Feature | `main.py (Ollama LLaMA-3)` | `app.py (Hugging Face BART)` |
|--------|----------------------------|------------------------------|
| PDF/HTML Upload | Yes | Yes |
| Hybrid Retrieval (BM25 + Semantic) | Yes | Yes |
| LLM Summarization | Ollama LLaMA 3 Local (`llama3.1:latest`) | Hugging Face BART (`facebook/bart-large-cnn`) |
| Streaming Output | Yes | Yes |
| Local Execution | Yes (Ollama) | Yes (CPU / Free) |

## Dataset / Test Document
Official Evaluation Document:
```
https://arxiv.org/pdf/2412.19437.pdf
```

## Technology Stack
- Python
- Flask
- Ollama LLaMA 3 (Local LLM)
- Hugging Face Transformers
- Sentence-Transformers
- Rank BM25
- Bootstrap 5 (Frontend)

## Installation
```bash
git clone https://github.com/kobeoseijnr/KobeRAG.git
cd KobeRAG
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Required Libraries
```bash
pip install flask transformers sentence-transformers rank_bm25 torch fitz bs4
```
Additionally for LLaMA version:
```bash
ollama pull llama3.1:latest
```

## Running the Application

### 1. Run LLaMA Local Version (`main.py`)
```bash
python main.py
```
- Uses **Ollama LLaMA 3 (`llama3.1:latest`)**
- Streams summarized response from local model

### 2. Run Hugging Face Free Version (`app.py`)
```bash
python app.py
```
- Uses **Hugging Face BART (`facebook/bart-large-cnn`)**
- Runs 100% **free**, CPU-only, fully local

## Frontend Highlights
- Bootstrap 5 UI
- PDF / HTML Upload
- Streaming QA Answer Section
- Modal Popup for Upload Success/Failure

## Example Q&A Output
**Question:** _"What is AI's role in smart cities?"_

**Streamed Answer:**
```
AI optimizes resources, enables real-time monitoring, and improves decision-making in smart cities.
```

## Deliverables
- `/upload` endpoint for document ingestion
- `/stream_ask` for streaming answers
- `main.py` → Ollama LLaMA 3 based RAG
- `app.py` → Hugging Face BART Summarization based RAG
- `index.html` → Clean Bootstrap Frontend with Modals

## Optimizations
- Hybrid Retrieval (BM25 + Semantic)
- Summarization for concise answers
- Word-by-word Streaming (No delay on large chunks)

## Future Enhancements
- Add spinner while streaming
- Store Q/A chat history
- Integrate FAISS for faster semantic search
- Option to download answer as text

## Author
**osei wusu brempong**

## License
MIT License
