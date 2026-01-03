from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'cost_usd', 'stock_quantity', 'category']
    list_filter = ['category', 'supplier_country']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']