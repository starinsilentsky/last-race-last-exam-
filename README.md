# Кондитерская «Сладкий рай» — Каталог тортов

Веб-приложение на Flask с SQLite. Реализует полный CRUD для таблицы тортов.

## Стек
- **Backend:** Python 3 + Flask
- **БД:** SQLite (файл `cakes.db` создаётся автоматически)
- **Шаблоны:** Jinja2 (HTML через `templates/`)
- **Стиль:** согласно руководству по стилю ДЭ (Times New Roman, #FC34C8, #31EBFF, #FFFFFF)

## Запуск

```bash
pip install flask
python app.py
```

Открыть в браузере: http://localhost:5000

## Функциональность

| Действие | URL |
|---|---|
| Просмотр каталога | GET `/` |
| Поиск, фильтр, сортировка | GET `/?search=...&brand=...&sort=...` |
| Добавить торт | GET/POST `/cake/new` |
| Редактировать торт | GET/POST `/cake/<id>/edit` |
| Удалить торт | POST `/cake/<id>/delete` |

## Структура проекта

```
cakes_app/
├── app.py              # Flask-приложение (маршруты, БД)
├── cakes.db            # SQLite (создаётся при первом запуске)
├── templates/
│   ├── base.html       # Базовый шаблон (шапка, стили)
│   ├── index.html      # Каталог тортов с фильтрами
│   └── form.html       # Форма добавления/редактирования
└── static/
    └── img/            # Фотографии тортов
```

## Таблица `cakes`

| Поле | Тип | Описание |
|---|---|---|
| id | INTEGER PK | Авто-ID |
| article | TEXT | Артикул (T001C1) |
| name | TEXT | Наименование |
| unit | TEXT | Единица измерения |
| price | REAL | Цена в рублях |
| brand | TEXT | Кондитерская |
| cake_type | TEXT | Тип торта |
| category | TEXT | Категория |
| discount | INTEGER | Скидка % |
| stock | INTEGER | Остаток на складе |
| description | TEXT | Описание |
| photo | TEXT | Имя файла фото |

При первом запуске БД заполняется 20 тортами из файла `tovar.xlsx`.
