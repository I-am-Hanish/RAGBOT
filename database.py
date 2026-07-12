"""
database.py
Handles SQLite chat history.
"""

import sqlite3
from config import DB_FILE


class ChatDatabase:

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    # --------------------------------------------
    # Save chat
    # --------------------------------------------
    def save_chat(self, user_message, bot_response):

        self.cursor.execute(
            """
            INSERT INTO chats(
                user_message,
                bot_response
            )
            VALUES (?, ?)
            """,
            (user_message, bot_response),
        )

        self.conn.commit()

    # --------------------------------------------
    # Get latest chats
    # --------------------------------------------
    def get_history(self, limit=10):

        self.cursor.execute(
            """
            SELECT
                user_message,
                bot_response,
                timestamp
            FROM chats
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return list(reversed(self.cursor.fetchall()))

    # --------------------------------------------
    # Clear history
    # --------------------------------------------
    def clear_history(self):

        self.cursor.execute("DELETE FROM chats")
        self.conn.commit()

    # --------------------------------------------
    # Close database
    # --------------------------------------------
    def close(self):
        self.conn.close()