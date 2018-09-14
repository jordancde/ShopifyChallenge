from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel
import graphene
from graphene_django import DjangoObjectType

class LineItem(DjangoObjectType):
    class Meta:
        model = LineItemModel

# also adds line item to product
class CreateLineItem(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int()
        product = graphene.Int()

    ok = graphene.Boolean()
    line_item = graphene.Field(lambda: LineItem)

    def mutate(self, info, quantity, product):

        productModel = ProductModel.objects.get(pk=product)

        lineItemModel = LineItemModel.objects.create(
            quantity=quantity,
            product=productModel,
            value = quantity*ProductModel.objects.get(pk=product).value
        )

        productModel.line_items.add(lineItemModel)
        productModel.save()
        
        line_item = LineItem(
            value=quantity*ProductModel.objects.get(pk=product).value,
            quantity=quantity,
            product=ProductModel.objects.get(pk=product)
        )

        ok = True
        return CreateLineItem(line_item=line_item, ok=ok)

# Update Line Item - DONT FORGET TO UPDATE LINE ITEMS VALUES and orders on product update
class UpdateLineItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        quantity = graphene.Int(required=False)
        product = graphene.Int(required=False)

    ok = graphene.Boolean()
    line_item = graphene.Field(lambda: LineItem)

    def mutate(self, info, id, quantity=None, product=None):

        lineItemModel = LineItemModel.objects.get(id=id)

        if quantity:
            lineItemModel.quantity = quantity

        if product:
            lineItemModel.product = ProductModel.objects.get(pk=product)

        if quantity or product:
            lineItemModel.recalculate_value()

            related_orders = OrderModel.objects.filter(line_items__in=[id])
            
            for order in related_orders:
                order.recalculate_value()

        lineItemModel.save()
        
        line_item = LineItem(
            value=lineItemModel.value,
            quantity=lineItemModel.quantity,
            product=lineItemModel.product
        )

        ok = True
        return UpdateLineItem(line_item=line_item, ok=ok)

# delete line item - updates order total value
class DeleteLineItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        lineItemModel = LineItemModel.objects.get(id=id)

        related_orders = OrderModel.objects.filter(line_items__in=[id])
        
        for order in related_orders:
            order.line_items.remove(lineItemModel)
            order.recalculate_value()

        lineItemModel.delete()

        ok = True
        return DeleteLineItem(ok=ok)