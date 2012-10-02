import datetime
from haystack.indexes import *
from haystack import site
from harga.models import Product


class ProductIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset_x(self):
        """Used when the entire index for model is updated."""
        return Product.objects.filter(modified__lte=datetime.datetime.now())


site.register(Product, ProductIndex)