"""
config.py
Central configuration for the Conversational RAG system.
"""

import os
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCUMENT_FOLDER = os.path.join(BASE_DIR, "documents")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
DB_FILE = os.path.join(BASE_DIR, "chat_history.db")
CHAT_STORE_FILE = os.path.join(BASE_DIR, "chat_store.json")
MANIFEST_FILE = os.path.join(BASE_DIR, "manifest.json")

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

# ============================================================
# VECTOR DATABASE
# ============================================================

COLLECTION_NAME = "rag_docs"

# ============================================================
# MODEL SETTINGS
# ============================================================

LLM_MODEL = "phi3:mini"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# ============================================================
# RAG SETTINGS
# ============================================================


SIMILARITY_TOP_K = 3
CHUNK_SIZE = 768
CHUNK_OVERLAP = 80
# ============================================================
# MEMORY SETTINGS
# ============================================================

MEMORY_TOKEN_LIMIT = 1500

# ============================================================
# OLLAMA
# ============================================================

OLLAMA_URL = "http://localhost:11434"

Settings.llm = Ollama(
    model=LLM_MODEL,
    base_url=OLLAMA_URL,
    request_timeout=120,
    additional_kwargs={
        "num_ctx": 2048,
        "num_predict": 256,
        "temperature": 0.2,
    },
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name=EMBED_MODEL
)

Settings.chunk_size = CHUNK_SIZE
Settings.chunk_overlap = CHUNK_OVERLAP