from django.contrib import admin
from django import forms

from harga.models import Product, ProductExtra

class ProductAdmin(admin.ModelAdmin):
    pass

class ProductExtraAdminForm(forms.ModelForm):
    class Meta:
        model = ProductExtra
        widgets = {
            'tarikh': forms.TextInput,
            'nama': forms.TextInput(attrs={'size': '80'}),
            'premis': forms.TextInput(attrs={'size': '80'}),
            'harga': forms.TextInput,
            'kawasan': forms.TextInput(attrs={'size': '80'}),
        }

class ProductExtraAdmin(admin.ModelAdmin):
    form = ProductExtraAdminForm

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductExtra, ProductExtraAdmin)
