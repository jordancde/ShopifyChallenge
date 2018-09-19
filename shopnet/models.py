
from django.db import models


# Django models, will be later interpreted as GraphQL models
class LineItemModel(models.Model):
    value = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE)

    # Recalculates the line item value based on product and quantity
    def recalculate_value(self):
        self.value = self.quantity*self.product.value
        self.save()

class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=7, decimal_places=2)
    line_items = models.ManyToManyField(LineItemModel)

class OrderModel(models.Model):
    buyer = models.CharField(max_length=100)
    line_items = models.ManyToManyField(LineItemModel)
    value = models.DecimalField(max_digits=7, decimal_places=2,null=True)

    # Recalculates the line item value based on sum of line item values
    def recalculate_value(self):
        total = 0
        for l in self.line_items.all():
            total += l.value
        self.value = total
        self.save()

class ShopModel(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(ProductModel)
    orders = models.ManyToManyField(OrderModel)

