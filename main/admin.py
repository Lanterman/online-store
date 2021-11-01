from django.contrib import admin

from main.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'description', 'price', 'stock_in', 'category')
    list_display = ('id', 'name', 'slug', 'price', 'stock_in', 'category')
    list_display_links = ('id', 'name', 'slug')
    list_filter = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    list_select_related = ('category',)
    actions = ['make_product_true', 'make_product_false']

    @admin.action(description='Добавить в наличие')
    def make_product_true(self, request, queryset):
        queryset.update(stock_in=True)
        self.message_user(request, "Появились в наличии.")

    @admin.action(description='Убрать из наличия')
    def make_product_false(self, request, queryset):
        queryset.update(stock_in=False)
        self.message_user(request, "Распроданы.")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('description', 'user', 'product')
    list_display = ('id', 'user', 'product', 'date')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'product', 'date')
    list_select_related = ('user', 'product')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    fields = ('user', 'product')
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'product')
    raw_id_fields = ('product',)
