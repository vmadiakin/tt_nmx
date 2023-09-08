from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from django_filters import rest_framework as django_filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer


class CategoryViewSet(ModelViewSet):
    """
    API для управления категориями товаров.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description="Удаление категории, если она не привязана к каким-либо товарам.",
        responses={204: "Успешное удаление", 400: "Неверный запрос"}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Удаление категории, если она не привязана к каким-либо товарам.
        """
        category = self.get_object()
        products_with_category = category.products.filter(is_deleted=False)
        if products_with_category.exists():
            return Response(
                {"detail": "Нельзя удалить категорию, которая привязана к товарам."},
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    """
    API для управления товарами.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter

    @swagger_auto_schema(
        operation_description="Создание нового товара с привязкой к категориям.",
        request_body=ProductCreateSerializer,
        responses={201: "Создано", 400: "Неверный запрос"}
    )
    def create(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        category_names = validated_data.get('category_names', [])

        if len(category_names) < 2 or len(category_names) > 10:
            return Response(
                {"detail": "Товар должен иметь от 2 до 10 категорий."},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Редактирование товара с привязкой к категориям.",
        request_body=ProductCreateSerializer,
        responses={201: "Создано", 400: "Неверный запрос"}
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductCreateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(ProductSerializer(product).data)

    @swagger_auto_schema(
        operation_description="Мягкое удаление товара.",
        responses={204: "Удалено", 400: "Неверный запрос"}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Мягкое удаление товара.
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
