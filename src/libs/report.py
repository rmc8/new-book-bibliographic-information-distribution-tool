import requests


def send_discord_webhook(
    webhook_url: str,
    title: str,
    author: str,
    keyword: str,
    amazon_url: str,
    books_or_jp_url: str,
):
    """
    DiscordのWebhookにメッセージを送信する関数

    Args:
        webhook_url (str): WebhookのURL
        title (str): 書籍のタイトル
        author (str): 著者名
        keyword (str): 検索キーワード
        amazon_url (str): Amazonの商品ページのURL
        books_or_jp_url (str): Books.or.jpの書籍のURL
    Returns (bool):
        成功時にTrueを返しそれ以外はFalseとなる
    """
    content = ""
    embed = {
        "color": 0x009999,
        "title": title,
        "fields": [
            {"name": "Author", "value": author},
            {"name": "Keyword", "value": keyword},
            {"name": "Amazon", "value": amazon_url, "inline": True},
            {"name": "Books.or.jp", "value": books_or_jp_url, "inline": True},
        ],
    }
    data = {
        "content": content,
        "flags": 4096,
        "embeds": [embed],
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=data, headers=headers)
    # Res check
    if response.status_code == 204:
        return True
    return False
