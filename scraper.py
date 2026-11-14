import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import re
import json


def http_get(url: str):
    """Обертка для GET-запросов с настроенным таймаутом и политикой ретрая

    Args:
        str: Запрашиваемый адрес

    Returs:
        Возвращает Response
    """

    session = requests.Session()

    # Настройка повторов: 3 попытки, задержка 0.5s, повторяем при 500/502/503/504
    # retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    retries = Retry(total=3, backoff_factor=0.5)

    # Подключаем адаптер к http и https
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session.get(url, timeout=10)

@dataclass
class BookData:
    """Специальный дата-класс для хранения информации о книге"""

    name: str  # Название
    price: float  # Цена
    rating: int  # Рейтинг
    amount_available: int  # Доступно экземпляров
    description: str  # Описание
    additional_info: dict[str, str]  # Дополнительная информация

def get_book_data(book_url: str) -> BookData:
    """Считывает информацию о книге с веб-страницы

    Args:
       str: путь к веб-странице книги

    Returns:
       Информация о книге в виде объекта дата-класса BookData
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    response = http_get(book_url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("article", class_="product_page")

    # вытаскиваем название книги из заголовка h1
    name = article.find("h1").get_text()

    # ищем тэг, содержащий цену, вытаскиваем значение, обрезаем знак валюты
    price = float(article.find("p", class_="price_color").get_text().replace("£", ""))

    # маппинг рейтинга текст -> число
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    # ищем тэг, хранящий оценку, вытаскиваем значение класса, преобразуем в число
    rating = rating_map[article.find("p", class_="star-rating")["class"][1]]

    # ищем тэг, соддержащий кол-во книг в наличии, регуляркой вытаскиваем число
    amount_available_data = article.find("p", class_="instock availability").get_text(
        strip=True
    )
    amount_available = int(re.search(r"\d+", amount_available_data).group())

    # ищем тег с айди product_description, само описание вытаскиваем из следующего тэга
    description_tag = article.find(id="product_description")
    description = (
        description_tag.find_next_sibling("p").get_text()
        if description_tag is not None
        else ""
    )

    # вспомогательную информацию с таблицы будем хранить в виде словаря в исходном виде для простоты
    table_tag = article.find("table")
    additional_info = {}
    for tr in table_tag.find_all("tr"):
        additional_info[tr.find("th").get_text()] = tr.find("td").get_text()

    return BookData(name, price, rating, amount_available, description, additional_info)
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ

def scrape_books(is_save: bool = False, pages: int = 50) -> list[BookData]:
    """Функция парсинга информации о книгах с сайта books.toscrape.com

    Args:
        is_save: Если True, сохраняет информацию о книгах в файл book_data.txt в формате JSON
        pages: Если указано, количество парсящихся страниц будет ограничено этим числом
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    result = []

    # Перебираем все 50 страниц каталога
    for n in range(1, pages + 1):
        print(f"Парсинг страницы {n}")
        response = http_get(f"http://books.toscrape.com/catalogue/page-{n}.html")
        soup = BeautifulSoup(response.content, "html.parser")

        # находим тэг-список и перебираем его элементы
        for li in soup.find("ol").find_all("li"):
            # ищем тэг-ссылку, передаём её значение в функцию парсинга веб-страницы о книге
            test = li.find("a")["href"]
            book_data = get_book_data(
                f"http://books.toscrape.com/catalogue/{li.find('a')['href']}"
            )
            #print(book_data)
            result.append(book_data)

        print(f"Конец парсинга страницы {n}")

    if is_save:
        with open("../artifacts/book_data.txt", "w", encoding="utf-8") as f:
            f.write(
                # Так как строгого требования к форматированию внутри файла не задано,
                # я решил форматировать в формате json, так как он наглядный и ходовой
                json.dumps([asdict(x) for x in result], ensure_ascii=False, indent=3)
            )
    return result

    # КОНЕЦ ВАШЕГО РЕШЕНИЯ