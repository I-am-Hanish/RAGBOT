"""
retriever.py

Creates the Conversational RAG chat engine.
"""

from llama_index.core.chat_engine.types import BaseChatEngine

from config import (
    SIMILARITY_TOP_K,
)

from memory import ConversationMemory
from indexer import IndexManager


class RAGChatbot:

    def __init__(self):

        # Persistent memory
        self.memory_manager = ConversationMemory()
        self.memory = self.memory_manager.get_memory()

        # Load or build index
        self.index = IndexManager().get_index()

        if self.index is None:
            self.chat_engine = None
        else:
            self.chat_engine = self.create_chat_engine()

    # -------------------------------------------------------
    # Create Chat Engine
    # -------------------------------------------------------

    def create_chat_engine(self) -> BaseChatEngine:

        return self.index.as_chat_engine(

            chat_mode="context",

            similarity_top_k=SIMILARITY_TOP_K,

            memory=self.memory,

            system_prompt="""
You are a Conversational Retrieval-Augmented Generation (RAG) assistant.

Rules:

1. Answer ONLY using the retrieved documents whenever possible.

2. Use previous conversation memory when it helps answer follow-up questions.

3. If the answer is not found in the documents, clearly say:

'I couldn't find that information in the indexed documents.'

4. Never invent facts.

5. Be concise but informative.

6. Mention the source document when possible.
""",

            verbose=False,
        )

    # -------------------------------------------------------
    # Ask
    # -------------------------------------------------------

    def ask(self, question):

        if self.chat_engine is None:

            return (
                "No documents are indexed.",
                []
            )

        response = self.chat_engine.chat(question)

        sources = []

        try:

            if hasattr(response, "source_nodes"):

                for node in response.source_nodes:

                    filename = node.metadata.get(
                        "file_name",
                        "Unknown"
                    )

                    page = node.metadata.get(
                        "page_label",
                        "-"
                    )

                    score = getattr(
                        node,
                        "score",
                        None
                    )

                    sources.append({

                        "file": filename,
                        "page": page,
                        "score": score

                    })

        except Exception:
            pass

        self.memory_manager.save()

        return str(response), sources

    # -------------------------------------------------------
    # Reset Memory
    # -------------------------------------------------------

    def clear_memory(self):

        self.memory_manager.reset()