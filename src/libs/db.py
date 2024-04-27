import sqlite3
from typing import List


class BookDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS books
                    (isbn TEXT PRIMARY KEY)"""
        )
        conn.commit()
        conn.close()

    def check_processed_books(self, isbn_list: List[str]) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        placeholders = ",".join(["?"] * len(isbn_list))
        c.execute(
            f"SELECT isbn FROM books WHERE isbn IN ({placeholders})",
            isbn_list,
        )
        processed_isbns = [row[0] for row in c.fetchall()]
        conn.close()
        return processed_isbns

    def insert_books(self, isbn_list: List[str]):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for isbn in isbn_list:
            c.execute("INSERT OR IGNORE INTO books (isbn) VALUES (?)", (isbn,))
        conn.commit()
        conn.close()
