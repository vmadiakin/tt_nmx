import csv
import os
from django.core.management import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Импорт данных из файлов CSV'

    def handle(self, *args, **options):
        # Получить базовый каталог вашего проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Составить абсолютные пути к файлам CSV
        categories_csv_path = os.path.join(base_dir, 'db_data', 'categories.csv')
        products_csv_path = os.path.join(base_dir, 'db_data', 'products.csv')
        product_categories_csv_path = os.path.join(base_dir, 'db_data', 'product_categories.csv')

        # Импорт категорий
        with open(categories_csv_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Пропустить заголовок
            for row in csvreader:
                Category.objects.create(name=row[1])

        # Импорт товаров
        with open(products_csv_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Пропустить заголовок
            for row in csvreader:
                # Создаем товар
                product = Product.objects.create(name=row[1], price=row[2], is_published=row[3], is_deleted=row[4])

                # Устанавливаем связи с категориями из файла product_categories.csv
                with open(product_categories_csv_path, 'r') as product_category_file:
                    product_category_reader = csv.reader(product_category_file)
                    next(product_category_reader)  # Пропустить заголовок
                    for pc_row in product_category_reader:
                        if pc_row[1] == row[0]:  # Если товар в файле product_categories.csv соответствует текущему товару
                            category_id = pc_row[2]  # Идентификатор категории из файла
                            category = Category.objects.get(id=category_id)
                            product.category.add(category)  # Добавляем категорию к товару

        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы'))
