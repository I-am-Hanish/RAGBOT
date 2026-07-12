"""
main.py

Entry point for the Conversational RAG.
"""

import os

from retriever import RAGChatbot
from database import ChatDatabase
from config import DOCUMENT_FOLDER

# ============================================================
# INITIALIZE
# ============================================================

db = ChatDatabase()

rag = RAGChatbot()

print("\n==========================================")
print("     🚀 Conversational RAG Ready")
print("==========================================")

print(f"\nDocuments Folder:\n{DOCUMENT_FOLDER}\n")

print("Commands")
print("------------------------------------------")
print("history")
print("clear")
print("list documents")
print("exit\n")

# ============================================================
# LOOP
# ============================================================

while True:

    question = input("You: ").strip()

    if not question:
        continue

    # --------------------------------------------------------

    if question.lower() == "exit":

        db.close()

        print("\nGoodbye!\n")

        break

    # --------------------------------------------------------

    if question.lower() == "clear":

        rag.clear_memory()

        print("\nConversation memory cleared.\n")

        continue

    # --------------------------------------------------------

    if question.lower() == "history":

        history = db.get_history()

        print()

        if not history:

            print("No chat history.\n")

            continue

        for user, bot, ts in history:

            print(f"[{ts}]")

            print("You :", user)

            print("Bot :", bot)

            print()

        continue

    # --------------------------------------------------------

    if question.lower() == "list documents":

        print()

        for root, _, files in os.walk(DOCUMENT_FOLDER):

            for file in files:

                print("-", file)

        print()

        continue

    # --------------------------------------------------------

    answer, sources = rag.ask(question)

    print("\nBot:\n")

    print(answer)

    if sources:

        print("\nSources")

        printed = set()

        for src in sources:

            key = (src["file"], src["page"])

            if key in printed:
                continue

            printed.add(key)

            print(f"• {src['file']}  (Page {src['page']})")

    db.save_chat(question, answer)

    print()