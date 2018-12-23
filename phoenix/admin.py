from django.contrib import admin

from phoenix.models import Category, Product, Page

class PageAdmin(admin.ModelAdmin):
    list_display = (
    'product',
    'image',
    'likes',
    )

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Page, PageAdmin)
