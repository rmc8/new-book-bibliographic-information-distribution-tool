import os
import time
from typing import List, Dict

import yaml
from pandas import DataFrame

from libs.ndl import NdlClient
from libs.db import BookDatabase
from libs.model.book_data import BookData
from libs.report import send_discord_webhook

path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(path, "settings.yaml"), "r", encoding="utf-8") as f:
    settings = yaml.safe_load(f)


def create_dataframe(books: List[BookData]) -> DataFrame:
    table: List[Dict[str, str]] = []
    for book in books:
        record: Dict[str, str] = {
            "title": book.title,
            "author": ", ".join(book.creators),
            "isbn": book.isbn,
            "keyword": book.keyword,
            "amazon": str(book.amazon),
            "books_or_jp": str(book.books_or_jp),
        }
        table.append(record)
    return DataFrame(table)


def main():
    nc = NdlClient()
    books = []
    for keyword in settings.get("keywords"):
        data = nc.get_new_publications(keyword)
        books.extend(data)
        time.sleep(1.0)
    df = create_dataframe(books)
    bd = BookDatabase(os.path.join(path, "books.db"))
    isbn_list = df.isbn.to_list()
    already_processed_isbn: List[str] = bd.check_processed_books(isbn_list)
    df = df[~df.isbn.isin(already_processed_isbn)]
    webhook_url: str = settings["discord"]["webhook"]
    isbns: List[str] = []
    for rec in df.to_dict("records"):
        if rec["isbn"] in isbns:
            continue
        success = send_discord_webhook(
            webhook_url,
            rec["title"],
            rec["author"],
            rec["keyword"],
            rec["amazon"],
            rec["books_or_jp"],
        )
        if success:
            isbns.append(rec["isbn"])
    bd.insert_books(isbns)


if __name__ == "__main__":
    main()
