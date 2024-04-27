from typing import List, Dict, Any

from pydantic import BaseModel, HttpUrl, Field


class BookData(BaseModel):
    title: str
    creators: List[str]
    isbn: str = Field(..., pattern=r"^[0-9]{13}$")
    keyword: str
    amazon: HttpUrl
    books_or_jp: HttpUrl

    @classmethod
    def from_book_info(
        cls,
        book_info: Dict[str, Any],
        keyword: str,
    ) -> "BookData":
        isbn10 = book_info["isbn10"]
        isbn13 = book_info["isbn13"]
        return cls(
            title=book_info["title"],
            creators=book_info["creators"],
            isbn=isbn13,
            keyword=keyword,
            amazon=f"https://amazon.co.jp/dp/{isbn10}",
            books_or_jp=f"https://www.books.or.jp/book-details/{isbn13}",
        )
