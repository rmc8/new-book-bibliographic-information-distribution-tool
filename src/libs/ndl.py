import urllib.parse
from datetime import date
from typing import List, Dict, Optional, Any

import requests
from bs4 import BeautifulSoup

from .model.book_data import BookData


class NdlClient:
    BASE_URL: str = "https://ndlsearch.ndl.go.jp/api/opensearch"
    today: date = date.today()

    @staticmethod
    def conv_isbn13_to_isbn10(isbn13: str) -> Optional[str]:
        """
        ISBN13の文字列を受け取り、ISBN10に変換した文字列を返す。

        Args:
            isbn13 (str): ISBN13の文字列

        Returns:
            Optional[str]: ISBN10の文字列 (ISBN13の形式が無効な場合はNone)
        """

        def calc_isbn10_check_digit(isbn10_base: str) -> str:
            """
            ISBN10のチェックディジットを計算する。

            Args:
                isbn10_base (str): ISBN10の本体部分 (先頭9桁)

            Returns:
                str: チェックディジット
            """
            total: int = sum(
                int(digit) * (10 - i) for i, digit in enumerate(isbn10_base)
            )
            remainder: int = total % 11
            check_digit: str = str(11 - remainder) if remainder else "0"
            return check_digit if remainder != 10 else "X"

        if len(isbn13) != 13 or not isbn13.isdigit():
            return

        body: str = isbn13[3:12]
        check_digit: str = calc_isbn10_check_digit(body)
        isbn10: str = body + check_digit
        return isbn10

    @staticmethod
    def _extract_book_info(rss_data: str) -> List[Dict[str, Any]]:
        """
        RSSデータから書籍情報を抽出する。

        Args:
            rss_data (str): RSSデータの文字列

        Returns:
            List[Dict[str, Any]]: 書籍情報のリスト
        """
        soup: BeautifulSoup = BeautifulSoup(rss_data, "lxml-xml")
        book_infos: List[Dict[str, Any]] = []
        for item in soup.find_all("item"):
            title: str = item.find("title").text
            creators: List[str] = [
                creator.strip()
                for creator in item.find("author").text.split(",")
                if "著・文・その他" not in creator
            ]
            isbn13_elm = item.find(
                "dc:identifier",
                {"xsi:type": "dcndl:ISBN13"},
            )
            if isbn13_elm is None:
                continue
            isbn13: str = isbn13_elm.text.replace("-", "")
            isbn10: Optional[str] = NdlClient.conv_isbn13_to_isbn10(isbn13)
            book_infos.append(
                {
                    "title": title,
                    "creators": creators,
                    "isbn10": isbn10,
                    "isbn13": isbn13,
                }
            )
        return book_infos

    def get_new_publications(self, keyword: str) -> List[BookData]:
        """
        指定されたキーワードで新刊情報を取得する。

        Args:
            keyword (str): 検索キーワード

        Returns:
            List[BookData]: 書籍情報のリスト
        """
        params: Dict[str, str] = {
            "title": urllib.parse.quote(keyword),
            "from": f"{self.today:%Y-%m}",
        }

        response: requests.Response = requests.get(
            self.BASE_URL,
            params=params,
        )
        response.raise_for_status()
        book_infos: List[Dict[str, Any]] = self._extract_book_info(
            response.text,
        )
        book_data_list: List[BookData] = [
            BookData.from_book_info(book_info, keyword)
            for book_info in book_infos
        ]
        return book_data_list
