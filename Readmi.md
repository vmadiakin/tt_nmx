# Документация Store API

## API для взаимодействия с товарами и категориями.

### Сущности
- Товары: Представляют собой продукты или товары, которые могут быть связаны с одной или несколькими категориями.
- Категории: Группируют товары по определенным характеристикам или тематикам.
- Товар-Категория: Связь между товарами и категориями, позволяющая одному товару принадлежать нескольким категориям.

### Реализация RESTful API

#### Товары

**Получение списка товаров:**
- Метод: GET
- Путь: /api/products/
- Параметры запроса (опционально):
  - name (строка): Фильтр по имени товара.
  - category_id (число): Фильтр по идентификатору категории.
  - category_name (строка): Фильтр по имени категории.
  - price_min (число): Фильтр по минимальной цене товара.
  - price_max (число): Фильтр по максимальной цене товара.
  - published (булево): Фильтр по опубликованным товарам.
  - deleted (булево): Фильтр по товарам, которые не были удалены.

**Создание Товаров:**
- Метод: POST
- Путь: /api/products/
- Описание: Создание нового товара. Параметры запроса включают в себя информацию о товаре (название, цена, опубликован ли и др.).

**Редактирование Товаров:**
- Метод: PUT или PATCH
- Путь: /api/products/{id}/
- Описание: Изменение существующего товара по его идентификатору.

**Удаление товаров:**
- Метод: DELETE
- Путь: /api/products/{id}/
- Описание: Удаление товара (пометка как удаленного) по его идентификатору.

#### Категории

**Создание категорий:**
- Метод: POST
- Путь: /api/categories/
- Описание: Создание новой категории. Параметры запроса включают в себя информацию о категории (название и др.).

**Удаление категорий:**
- Метод: DELETE
- Путь: /api/categories/{id}/
- Описание: Удаление категории. Если категория прикреплена к товару, вернуть ошибку.

### Используемые технологии и библиотеки:
- Python: 3.11
- Django: 4.2.5
- Django REST framework (DRF): 3.14
- Docker Compose: Для управления Docker-контейнерами и развертывания приложения.
- PostgreSQL: Версия 15.0 используется как база данных.

## Спецификация API:
- [Посмотреть спецификацию API (Swagger)](http://127.0.0.1:8000/swagger/)
- [Посмотреть спецификацию API (ReDoc)](http://127.0.0.1:8000/redoc/)

## Инструкция по запуску проекта:

1. Установите Poetry, если вы его ещё не установили, выполнив следующую команду: 
`pip poetry install`

2. Установите зависимости, выполнив следующую команду:
`poetry install`
Эта команда прочитает файл `pyproject.toml` и установит все зависимости в виртуальное окружение вашего проекта.

3. Создайте файл `.env` в корневой директории проекта и укажите необходимые значения для переменных окружения, такие как настройки базы данных, секретный ключ и другие.

4. Примените миграции базы данных, выполнив следующую команду:
`python manage.py migrate`

5. апустите проект с помощью следующей команды: 
`python manage.py runserver`

6. Откройте браузер и перейдите по адресу `http://localhost:8000` чтобы получить доступ к Store API.

7. Убедитесь, что у вас установлена Python версии 3.11 и база данных Postgres работает корректно перед запуском проекта.

## Коллекция PostMan:
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/25635753-084640f3-7254-401f-abbf-56e90f372c75?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D25635753-084640f3-7254-401f-abbf-56e90f372c75%26entityType%3Dcollection%26workspaceId%3D54abe847-add9-4603-87d4-e3de18cf462e)

## Контакты:
<p>
  <a href="https://www.linkedin.com/in/vmadiakin/"><img alt="Linkedin" title="Vitalii Madiakin Linkedin" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>
  <a href="https://github.com/vmadiakin"><img alt="Github" title="Vitalii Madiakin Github" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://web.facebook.com/vmadiakin"><img alt="Facebook" title="Vitalii Madiakin FB" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white"></a>
  <a href="https://instagram.com/vmadiakin"><img alt="Instagram" title="Vitalii Madiakin Instagram" src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white"></a>
  <a href="mailto:vmadiakin@gmail.com"><img alt="Gmail" title="Vitalii Madiakin Gmail" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"></a>
  <a href="https://t.me/vmadiakin"><img alt="Telegram" title="Vitalii Madiakin Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a> 
</p>