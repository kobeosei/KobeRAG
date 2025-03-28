import time

from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import os
import fitz
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from rank_bm25 import BM25Okapi
import torch
from langchain_ollama import OllamaLLM  # Optional for local summarization but takes so much time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

embedder = SentenceTransformer('all-MiniLM-L6-v2')
document_chunks = []
bm25_corpus = []
bm25 = None
chunk_embeddings = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    global document_chunks, chunk_embeddings, bm25_corpus, bm25
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Extract text
    text = ""
    if filename.lower().endswith(".pdf"):
        doc = fitz.open(filename)
        for page in doc:
            text += page.get_text()
    elif filename.lower().endswith(".html"):
        with open(filename, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text()
    else:
        return jsonify({"error": "Only PDF and HTML supported"}), 400

    if not text.strip():
        return jsonify({"error": "Document is empty"}), 400

    # Chunk text (longer for better context)
    document_chunks = [text[i:i + 1500] for i in range(0, len(text), 1500)]
    chunk_embeddings = embedder.encode(document_chunks, convert_to_tensor=True)

    # BM25 Tokenization
    bm25_corpus = [chunk.lower().split() for chunk in document_chunks]
    bm25 = BM25Okapi(bm25_corpus)

    return jsonify({"message": "Document uploaded and indexed with hybrid retrieval"}), 200

@app.route("/stream_ask", methods=["POST"])
def stream_answer():
    global document_chunks, chunk_embeddings, bm25
    data = request.json
    question = data.get("question")

    if not document_chunks or chunk_embeddings is None:
        return jsonify({"answer": "Please upload a document first."}), 400

    # Semantic Scoring
    question_embedding = embedder.encode(question, convert_to_tensor=True)
    semantic_scores = util.cos_sim(question_embedding, chunk_embeddings)[0]

    # BM25 Scoring
    tokenized_query = question.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)

    # Hybrid scoring (simple weight example)
    hybrid_scores = 0.5 * semantic_scores.cpu().numpy() + 0.5 * bm25_scores
    best_idx = hybrid_scores.argmax()

    # Merge surrounding chunks
    start = max(0, best_idx - 1)
    end = min(len(document_chunks), best_idx + 2)
    context_chunk = " ".join(document_chunks[start:end])

    # Summarize the answer with Ollama LLaMA-3 (OR you can replace with OpenAI if needed)
    llm = OllamaLLM(model="llama3.1:latest")
    prompt = f"""
    You are a helpful assistant. Given the following context, answer the question concisely and accurately.

    Context: {context_chunk}

    Question: {question}

    Answer:
    """

    def generate():
        # Streaming LLM Response
        response = llm.invoke(prompt)
        # Optional: yield word by word
        for word in response.split():
            yield word + " "
            time.sleep(0.02)

    return Response(stream_with_context(generate()), content_type='text/plain')

if __name__ == "__main__":
    app.run(debug=True)
