import datetime
from haystack.indexes import *
from haystack import site
from harga.models import Product, ProductExtra


class ProductIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    tarikh = DateField(model_attr='tarikh_iso')

    def index_querysetx(self):
        """Used when the entire index for model is updated."""
        return Product.objects.filter(modified__lte=datetime.datetime.now())

class ProductExtraIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    tarikh = DateField(model_attr='tarikh_iso')

site.register(Product, ProductIndex)
site.register(ProductExtra, ProductExtraIndex)
