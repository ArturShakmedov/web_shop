from .models import *
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

# Сериализация - процесс формирования объекта из базы данных в вид JSON
# class CollectionSerializer(serializers.Serializer):
#     # Поля которые мы хотим видеть в ответе
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
    # Поле которого нет в базе, при этом его нельзя менять. Только читать

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6,
#                                      decimal_places=2,
#                                      source='unit_price')
#     # На фронт будет отправляться ключ price, но поле у нас unit_price
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax'
#     )

    # def calculate_tax(self, product: Product):
    #     return round(product.unit_price * Decimal(1.1), 2)
    #     # Округленная цена с наценкой 10% до 2х знаков после запятой
    #
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description',
                  'slug', 'inventory', 'price_with_tax', 'collection', 'images']

    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all() # Будем показывать id категории
    )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name='collection-detail'
    # )
    price = serializers.DecimalField(max_digits=6,
                                          decimal_places=2,
                                          source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax'
    )

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)
        # Округленная цена с наценкой 10% до 2х знаков после запятой

    def create(self, validated_data):
        product = Product(**validated_data)
        # Создать продукт на основе словаря
        product.other = 1
        product.save()
        return product

    #               Объект         новые данные
    def update(self, instance, validated_data):
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)

'''
cart/27bda4c0-3577-4188-be11-a9e3cc808dbe/

{
    'id': 27bda4c0-3577-4188-be11-a9e3cc808dbe,
    'items': [
        {
            'id': 1,
            'quantity': 10,
            'total_price': 1000,
            'product':  {
                "id": 1002,
                "title": "7up Diet, 355 Ml123",
                "price": 100,
            } 
        },
    ],
    'total_price': 1000
}


'''

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    # Попробуйте реализовать метод,
    # который считает всю стоимость корзины по ее товарам
    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


# Сериализер для добавления товара в корзину
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    # Поле, которое нужно выводить
    def validate_product_id(self, value):
        # Валидация product_id, проверяет существует ли продукт с этим ID
        if not Product.objects.filter(pk=value).exists():
            # Если продует не найдет, выбрасывается ошибка валидации
            raise serializers.ValidationError('Нет товара с данным id')
        # Если продукт существует, возвращается значение ID
        return value

    def save(self, **kwargs):
        # Получаем ID корзины из контекста запроса
        cart_id = self.context['cart_id']
        # Получаем ID продукта из проверенных данных
        product_id = self.validated_data['product_id']
        # Получаем кол-во добавляемого товара
        quantity = self.validated_data['quantity']

        try:
            # Попытка найти существующий элемент в корзине с данными
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # Если элемент найдет, увеличиваем кол-во
            cart_item.quantity += quantity
            cart_item.save()
            # Обновляем instance сериалайзера наденным элементом
            self.instance = cart_item
        except:
            # Если элемент не найдет, создаем новый с заданными параметрами
            self.instance = CartItem.objects.create(cart_id=cart_id,
                                                    **self.validated_data)
        # Возвращаем экземпляр модели
        return self.instance

    class Meta:
        # Указываем, что моделью для сериализатора является CartItem
        model = CartItem
        # Определяем какие поля будут включены в сериализацию
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Не существующий ID корзины')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('Корзина пустая')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(
                cart_id=cart_id
            )

            order_items = [OrderItem(
                order=order,
                product=item.product,
                unit_price=item.product.unit_price,
                quantity=item.quantity
            ) for item in cart_items]
            # Надо сразу закинуть список объектов в базу данных
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            return order

