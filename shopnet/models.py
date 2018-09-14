
from django.db import models

class LineItemModel(models.Model):
    value = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)

class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    line_items = models.ManyToManyField(LineItemModel)

class OrderModel(models.Model):
    buyer = models.CharField(max_length=100)
    line_items = models.ManyToManyField(LineItemModel)
    value = models.DecimalField(max_digits=7, decimal_places=2,null=True)

class ShopModel(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(ProductModel)
    orders = models.ManyToManyField(OrderModel)

