"""
memory.py

Handles persistent conversation memory.
"""

import os

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore

from config import CHAT_STORE_FILE, MEMORY_TOKEN_LIMIT


class ConversationMemory:

    def __init__(self):

        if os.path.exists(CHAT_STORE_FILE):
            self.chat_store = SimpleChatStore.from_persist_path(
                CHAT_STORE_FILE
            )
        else:
            self.chat_store = SimpleChatStore()

        self.memory = ChatMemoryBuffer.from_defaults(
            token_limit=MEMORY_TOKEN_LIMIT,
            chat_store=self.chat_store,
            chat_store_key="user",
        )

    def get_memory(self):
        return self.memory

    def save(self):
        self.chat_store.persist(
            persist_path=CHAT_STORE_FILE
        )

    def reset(self):
        self.memory.reset()
        self.save()