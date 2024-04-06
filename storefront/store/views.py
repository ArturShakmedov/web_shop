from django.shortcuts import get_object_or_404
from .models import *
from django.http import HttpResponse
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer

# Create your views here.
# def product_list(request):
#     return HttpResponse('Ok')

# @api_view()
# def product_list(request):
#     return Response('Ok')


# @api_view()
# def collection_list(request):
#     queryset = Collection.objects.all()  # Что выводим
#     serializer = CollectionSerializer(queryset, many=True,
#                                       context={'request': request})
#     # Собираем JSON из объектов базы и отправляем в ответ
#     return Response(serializer.data)
#
# @api_view()
# def collection_detail(request, pk):
#     collection = Collection.objects.get(pk=pk)
#     serializer = CollectionSerializer(collection,
#                                       context={'request': request})
#     return Response(serializer.data)

# @api_view()
# def product_list(request):
#     queryset = Product.objects.all()
#     serializer = ProductSerializer(queryset, many=True,
#                                    context={'request': request})
#     return Response(serializer.data)
#
#
# @api_view()
# def product_detail(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except:
#         # return Response(status=404)
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
# @api_view(['GET', 'POST'])  # Показ всего и Создание нового
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(
#             products_count=Count('products').all() # Дополнительное поле
#         )
#         serializer = CollectionSerializer(queryset, many=True,
#                                           context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # Создаем новую категорию
#         serializer = CollectionSerializer(data=request.data) # Принимаем данные
#         serializer.is_valid(raise_exception=True) # Короткая версия if is_valid()
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
#
# @api_view(['GET', 'PUT', 'DELETE']) # Показ, Изменение, Удаление
# def collection_detail(request, pk):
#     collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data,
#                                           context={'request': request})
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({
#                 'error': 'Категория не может быть удалена. Так как в ней есть товар'
#             }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True,
#                                        context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data,
#                                        context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product,
#                                        context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data,
#                                        context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Товар нельзя удалить. Так как он есть в заказах'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView

# class ProductList(APIView):
#
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         # select_related - для оптимизации запросов в связанных моделях
#         serializer = ProductSerializer(queryset, many=True,
#                                        context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data,
#                                        context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product,
#                                         context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSerializer(product, data=request.data,
#                                        context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': 'Товар нельзя удалить. Так как он есть в заказах'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class CollectionList(APIView):
#     def get(self, request):
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True,
#                                           context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
#
# class CollectionDetail(APIView):
#     def get(self, request, pk):
#         collection = Collection.objects.annotate(
#             products_count=Count('products')).get(pk=pk)
#         serializer = CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         collection = Collection.objects.annotate(
#             products_count=Count('products')).get(pk=pk)
#         serializer = CollectionSerializer(collection, data=request.data,
#                                           context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
#         if collection.product_set.count() > 0:
#             return Response({'error': 'Категория не может быть удалена. '
#                                       'Так как в ней есть товары'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductList(ListCreateAPIView):
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    #
    # def get_serializer_class(self):
    #     return ProductSerializer
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Товар нельзя удалить. Так как он есть в заказах'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.annotate(products_count=Count('products')).all()

    def delete(self, request, pk):
        collection = Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
        if collection.product_set.count() > 0:
            return Response({'error': 'Категория не может быть удалена. '
                                      'Так как в ней есть товары'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('collection').all()
    pagination_class = DefaultPagination

    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Товар не может быть удален. Так как он есть в заказах'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    permission_classes = [IsAdminOrReadOnly]


    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Категория не может быть удалена. Так '
                                      'как в ней есть товары'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(self, request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # Указываем какие отзывы выводим
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import (CartSerializer, CartItemSerializer,
                          AddCartItemSerializer, UpdateCartItemSerializer)

class CartViewSet(CreateModelMixin, RetrieveModelMixin,
                  DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


# cb869998-76f4-428a-a569-d1b9caa73e18

# djoser
# pip install djoser

from .serializers import CustomerSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    # customers/me как и users/me
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            customer = Customer.objects.get(user_id=request.user.id)
        except:
            customer, created = Customer.objects.get_or_create(user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


from .serializers import OrderSerializer, OrderItemSerializer
from .serializers import CreateOrderSerializer, UpdateOrderSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data,
                                           context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        # Если админ - можно видеть все заказы
        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
        # Если это простой смертный - то возвращаем только ЕГО заказы

