# RAGBOT Complete Setup Guide

## Prerequisites
- Python 3.11+
- Git
- Ollama
- 8GB RAM minimum (16GB recommended)

## Clone
```bash
git clone https://github.com/YOUR_USERNAME/RAGBOT.git
cd RAGBOT
```

## Virtual Environment
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you don't have requirements.txt:
```bash
pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface llama-index-vector-stores-chroma chromadb sentence-transformers transformers torch huggingface-hub ollama pypdf python-docx pandas numpy openpyxl tqdm requests
```

## Install Ollama
Download from https://ollama.com

```bash
ollama --version
ollama serve
ollama pull phi3:mini
ollama list
```

## Supported Documents
- PDF
- DOCX
- TXT

Place them in `documents/`.

## Run
```bash
python main.py
```

## Troubleshooting
- ModuleNotFoundError → `pip install -r requirements.txt`
- Failed to connect to Ollama → `ollama serve`
- Readonly ChromaDB → delete `chroma_db/` and rerun.

## Technologies
Python, LlamaIndex, ChromaDB, Ollama, Hugging Face, Sentence Transformers, PyPDF, python-docx.
