from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='категория товара')

    class Meta:
        verbose_name = 'категория товаров'
        verbose_name_plural = 'категории товаров'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='название товара')
    category = models.ManyToManyField(Category, verbose_name='категория', related_name='products', db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True, verbose_name='цена', validators=[
            MinValueValidator(Decimal('0.00'), message='Цена товара должна быть >= 0.')])
    is_published = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name}'
