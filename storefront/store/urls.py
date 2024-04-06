from django.urls import path
from . import views
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# router = DefaultRouter()
# router.register('products', ProductViewSet)
# router.register('collections', CollectionViewSet)
# urlpatterns = router.urls

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product') # product_pk
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')
urlpatterns = router.urls + products_router.urls + carts_router.urls

# product/1/reviews
# Вложенность моделей путей

# pip install drf-nested-routers

#
# urlpatterns = [
#     path('products/', ProductList.as_view(), name='product-list'),
#     path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
#     path('collections/', CollectionList.as_view(), name='collection-list'),
#     path('collection/<int:pk>/', CollectionDetail.as_view(), name='collection-detail')
# ]