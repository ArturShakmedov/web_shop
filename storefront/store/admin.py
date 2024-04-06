from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10) # Меньше чем 10


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '': # Если есть картинка
            return format_html(f'<img src="{instance.image.url}" width="75px">')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title'] # Поле slug Будет заполняться на основе title
        # Пылесосы -> pilesosy
    }
    list_display = ['title', 'unit_price', 'inventory_status',
                    'collection']
    list_editable = ['unit_price']
    inlines = [ProductImageInline]
    list_per_page = 10  # 10 шт на страницу
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
            'collection__id': str(collection.id)
        })
        )
        return format_html(f'<a href="{url}">{collection.products_count}</a>')


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )
