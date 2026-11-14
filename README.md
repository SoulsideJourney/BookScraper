# BookScraper

## Описание проекта

Небольшой учебный проект на Python для сбора данных о книгах
с демонстрационного сайта [books.toscrape.com](https://books.toscrape.com/).

## Установка и запуск

### 1. Клонирование и окружение

```bash
git clone https://github.com/SoulsideJourney/BookScraper
cd books_scraper
python -m venv .venv
```

Активация окружения:

**Windows (Git Bash):**
```bash
source .venv/Scripts/activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Запуск ноутбука

Откройте `notebooks/HW_03_python_ds_2025.ipynb` в VS Code или Jupyter.
Перед запуском выберите kernel, указывающий на `.venv`
(`Select Kernel` → `Python Environment` → `.venv`).


## Структура репозитория

```
  books_scraper/
  ├── artifacts/
  │   └── books_data.txt                # результат работы скрапера (данные о книгах)
  ├── notebooks/
  │   └── HW_03_python_ds_2025.ipynb    # ноутбук с решенными заданиями
  ├── scraper.py                        # основной код
  ├── README.md                         # файл описания проекта
  ├── tests/
  │   └── test_scraper.py               # тесты
  ├── .gitignore                        # что не отслеживается git
  └── requirements.txt                  # список зависимостей проекта
  ```

Кратко, что где искать:

- **`scraper.py`** — точка входа. Здесь функция `get_book_data` (получение данных
  о книге по URL) и логика сохранения в `artifacts/`, а также планировщик запуска.
- **`artifacts/books_data.txt`** — итоговый файл с собранными данными.
  Перезаписывается при каждом запуске скрапера.
- **`notebooks/`** — ноутбук с демонстрацией работы `get_book_data` и разбором
  собранных данных.
- **`tests/`** — автотесты. Запускаются через `python -m pytest` из корня проекта.
- **`requirements.txt`** — зависимости; устанавливаются одной командой
  `pip install -r requirements.txt`.

## Документация

Используемые библиотеки и инструменты:

- [requests](https://requests.readthedocs.io/) — HTTP-запросы
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — парсинг HTML
- [schedule](https://schedule.readthedocs.io/) — запуск задач по расписанию
- [pytest](https://docs.pytest.org/) — тестирование
- [books.toscrape.com](https://books.toscrape.com/) — источник данных
  (демо-сайт для обучения парсингу)

Автор:

- **Имя Фамилия** — <email@example.com> — GitHub: [@username](https://github.com/username)
