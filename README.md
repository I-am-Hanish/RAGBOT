# RAGBOT – Intelligent Conversational RAG Chatbot

## Overview
RAGBOT is a Retrieval-Augmented Generation (RAG) chatbot that answers questions over your own documents using LlamaIndex, ChromaDB, and Ollama.

## Features
- Automatic indexing of new/modified/deleted documents
- Conversational chat with persistent memory
- Semantic search using embeddings
- Supports PDF, DOCX, and TXT
- Cross-platform (Windows/Linux)

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/RAGBOT.git
cd RAGBOT
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Ollama, start it, then download a model:

```bash
ollama serve
ollama pull phi3:mini
```

Place documents in `documents/` and run:

```bash
python main.py
```

For complete setup instructions, see **SETUP_GUIDE.md**.
