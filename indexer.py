"""
indexer.py

Builds, loads and automatically synchronizes the Chroma vector database.
"""

import os
import shutil
import chromadb

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
)

from llama_index.vector_stores.chroma import ChromaVectorStore

from config import (
    DOCUMENT_FOLDER,
    CHROMA_PATH,
    COLLECTION_NAME,
)

from sync import FileSynchronizer


class IndexManager:

    def __init__(self):

        self.sync = FileSynchronizer()

        self.db = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.db.get_or_create_collection(
            COLLECTION_NAME
        )

        self.vector_store = ChromaVectorStore(
            chroma_collection=self.collection
        )

    # ---------------------------------------------------------
    # Storage Context
    # ---------------------------------------------------------

    def storage_context(self):

        return StorageContext.from_defaults(
            vector_store=self.vector_store
        )

    # ---------------------------------------------------------
    # Load Documents
    # ---------------------------------------------------------

    def load_documents(self):

        if not os.path.exists(DOCUMENT_FOLDER):
            os.makedirs(DOCUMENT_FOLDER)

        files = []

        for root, _, filenames in os.walk(DOCUMENT_FOLDER):
            for file in filenames:
                files.append(os.path.join(root, file))

        if len(files) == 0:

            print("\n⚠️ No documents found.")

            return []

        documents = SimpleDirectoryReader(
            DOCUMENT_FOLDER
        ).load_data()

        print(f"\nLoaded {len(documents)} document(s)")

        return documents

    # ---------------------------------------------------------
    # Build Index
    # ---------------------------------------------------------

    def build_index(self):

        documents = self.load_documents()

        if len(documents) == 0:
            return None

        print("\n🔄 Building Vector Index...\n")

        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context(),
            show_progress=True,
        )

        print("\n✅ Index Created Successfully")

        return index

    # ---------------------------------------------------------
    # Load Existing Index
    # ---------------------------------------------------------

    def load_index(self):

        print("\n⚡ Loading Existing Index...")

        index = VectorStoreIndex.from_vector_store(
            self.vector_store
        )

        print("✅ Index Loaded")

        return index

    # ---------------------------------------------------------
    # Delete Existing Database
    # ---------------------------------------------------------

    def clear_database(self):

    # Close the current client first
        try:
            del self.collection
            del self.vector_store
            del self.db
        except Exception:
            pass

        import gc
        gc.collect()

        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH, ignore_errors=True)

        self.db = chromadb.PersistentClient(path=CHROMA_PATH)

        self.collection = self.db.get_or_create_collection(
            COLLECTION_NAME
        )

        self.vector_store = ChromaVectorStore(
            chroma_collection=self.collection
        )

    # ---------------------------------------------------------
    # Main Function
    # ---------------------------------------------------------

    def get_index(self):

        changed = self.sync.changes_detected()

        if changed:

            print("\n📄 Document changes detected.")

            self.clear_database()

            return self.build_index()

        if self.collection.count() == 0:

            print("\n📄 No existing index found.")

            return self.build_index()

        return self.load_index()