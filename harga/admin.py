from django.contrib import admin

from harga.models import Product, ProductExtra

class ProductAdmin(admin.ModelAdmin):
    pass

class ProductExtraAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductExtra, ProductExtraAdmin)
