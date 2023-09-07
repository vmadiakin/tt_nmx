from rest_framework import filters
from django_filters import rest_framework as django_filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        products_with_category = category.products.filter(is_deleted=False)
        if products_with_category.exists():
            return Response(
                {"detail": "Нельзя удалить категорию, которая прикреплена к товарам."},
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        # Парсим данные из запроса с использованием нового сериализатора
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем данные из сериализатора
        validated_data = serializer.validated_data
        category_names = validated_data.get('category_names', [])

        # Проверяем количество категорий
        if len(category_names) < 2 or len(category_names) > 10:
            return Response(
                {"detail": "Товар должен принадлежать от 2 до 10 категорий."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем категории, если они не существуют
        categories = []
        for category_name in category_names:
            category, created = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        # Создаем товар с категориями
        product = Product.objects.create(
            name=validated_data['name'],
            price=validated_data['price'],
            is_published=validated_data['is_published'],
            is_deleted=validated_data['is_deleted']
        )
        product.category.set(categories)

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
