from django.contrib import admin
from .models import *


class GoodAdmin(admin.ModelAdmin):

    list_display = ('name', 'options', 'description')
    search_fields = ('name', )
    list_filter = ('name', )


class ProductAdmin(admin.ModelAdmin):

    list_display = ('good', 'amount')
    search_fields = ('good__name', )
    list_filter = ('amount', )

admin.site.register(Good, GoodAdmin)
admin.site.register(Product, ProductAdmin)
