from rest_framework import serializers
from store.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        category = self.instance
        products_with_category = category.products.filter(is_deleted=False)
        if products_with_category.exists():
            raise serializers.ValidationError('Нельзя удалить категорию, которая прикреплена к товарам.')


class ProductSerializer(serializers.ModelSerializer):
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'is_published', 'is_deleted', 'category_names')

    def get_category_names(self, obj):
        return [category.name for category in obj.category.all()]


class ProductListSerializer(serializers.ModelSerializer):
    category_ids = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    category_names = serializers.ListSerializer(child=serializers.CharField(), required=False)
    min_price = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)

    class Meta:
        model = Product
        fields = ('name', 'category_ids', 'category_names', 'min_price', 'max_price', 'is_published', 'is_deleted')


class ProductCreateSerializer(serializers.ModelSerializer):
    category_names = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Product
        fields = ('name', 'price', 'category_names', 'is_published', 'is_deleted')
        extra_kwargs = {
            'category_names': {'required': True, 'help_text': 'Список имен категорий товара'},
        }

    def create(self, validated_data):
        category_names = validated_data.pop('category_names', [])
        product = Product.objects.create(**validated_data)

        categories = []
        for category_name in category_names:
            category, created = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        product.category.set(categories)
        return product

    def update(self, instance, validated_data):
        category_names = validated_data.pop('category_names', [])
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()

        categories = []
        for category_name in category_names:
            category, created = Category.objects.get_or_create(name=category_name)
            categories.append(category)

        instance.category.set(categories)
        return instance
