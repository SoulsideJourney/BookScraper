import pytest

# import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd().parent))

import scraper

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_fetched_books_count_is_correct():
    """Проверка, соответствует ли количество собранных книг ожидаемому значению"""

    # По 20 книг на страницу
    assert len(scraper.scrape_books(pages=1)) == 20
    assert len(scraper.scrape_books(pages=2)) == 40
    assert len(scraper.scrape_books(pages=0)) == 0


def test_fetched_book_data_is_correct():
    """Проверяем работоспособность функции парсинга страницы книги,
    значения полей должны соответствовать ожидаемым"""

    book_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    data = scraper.get_book_data(book_url)

    assert data.name == "A Light in the Attic"

    # Помимо самого названия, проверяется и корректное отделение символа валюты
    assert data.price == 51.77

    # Тут я понял, что забыл к int и float привести. Явные указания типов полей в классе,
    # похоже, ничего не дают
    assert data.rating == 3

    # То же самое, должно быть корректное срабатывание регулярки
    assert data.amount_available == 22


def test_fetched_book_additional_data_is_correct():
    book_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )
    data = scraper.get_book_data(book_url)

    # Словарь со вспомогательной информацией не пустой
    assert len(data.additional_info) != 0

    assert data.additional_info["UPC"] == "a897fe39b1053632"
    assert data.additional_info["Price (excl. tax)"] == "£51.77"
    assert data.additional_info["Number of reviews"] == "0"
