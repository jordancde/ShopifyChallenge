from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel
import graphene
from graphene_django import DjangoObjectType

class Order(DjangoObjectType):
    class Meta:
        model = OrderModel

class CreateOrder(graphene.Mutation):
    class Arguments:
        buyer = graphene.String()
        line_items = graphene.List(graphene.Int,required=False)

    ok = graphene.Boolean()
    order = graphene.Field(lambda: Order)

    def mutate(self, info, buyer, line_items=None):
        orderModel = OrderModel.objects.create(buyer=buyer)

        # If a list of line itema is providedm adds models referenced by ids to order
        if line_items is not None:
            for l in line_items:
                line_model = LineItemModel.objects.get(pk=l)
                orderModel.line_items.add(line_model)

            # Recalculates the order value with the new line items
            orderModel.recalculate_value()

        orderModel.save()

        order = Order(
            value=orderModel.value,
            buyer=buyer, 
            line_items=orderModel.line_items.all()
        )

        ok = True
        return CreateOrder(order=order, ok=ok)
    
# Update Order
class UpdateOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        buyer = graphene.String(required=False)
        line_items = graphene.List(graphene.Int,required=False)

    ok = graphene.Boolean()
    order = graphene.Field(lambda: Order)

    def mutate(self, info, id, buyer=None, line_items=None):
        orderModel = OrderModel.objects.get(id=id)
        
        if buyer:
            orderModel.buyer = buyer

        # Clears existing line items, then adds from new list
        if line_items is not None:
            orderModel.line_items.clear()
            
            for l in line_items:
                orderModel.line_items.add(LineItemModel.objects.get(pk=l))

            # Recalculates value based on new line items
            orderModel.recalculate_value()        
        
        orderModel.save()
        
        order = Order(
            buyer=orderModel.buyer,
            value=orderModel.value,
            line_items=orderModel.line_items.all()
        )

        ok = True
        return UpdateOrder(order=order, ok=ok)


# delete order - deletes associated line items
class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        orderModel = OrderModel.objects.get(id=id)

        # Deletes line items associated with order
        for line_item in orderModel.line_items.all():
            line_item.delete()

        orderModel.delete()

        ok = True
        return DeleteOrder(ok=ok)

# Add line item to order and update value
class AddLineItemToOrder(graphene.Mutation):
    class Arguments:
        line_item_id = graphene.Int(required=True)
        order_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    order = graphene.Field(lambda: Order)

    def mutate(self, info, line_item_id, order_id):
        lineItemModel = LineItemModel.objects.get(id=line_item_id)
        orderModel = OrderModel.objects.get(id=order_id)

        orderModel.line_items.add(lineItemModel)

        orderModel.recalculate_value()

        order = Order(
            id=orderModel.id,
            buyer=orderModel.buyer,
            value=orderModel.value,
            line_items=orderModel.line_items
        )

        ok = True
        return AddLineItemToOrder(ok=ok, order=order)



# Remove line item from order and update value
class RemoveLineItemFromOrder(graphene.Mutation):
    class Arguments:
        line_item_id = graphene.Int(required=True)
        order_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    order = graphene.Field(lambda: Order)

    def mutate(self, info, line_item_id, order_id):
        lineItemModel = LineItemModel.objects.get(id=line_item_id)
        orderModel = OrderModel.objects.get(id=order_id)

        orderModel.line_items.remove(lineItemModel)

        orderModel.recalculate_value()

        order = Order(
            id=orderModel.id,
            buyer=orderModel.buyer,
            value=orderModel.value,
            line_items=orderModel.line_items
        )

        ok = True
        return RemoveLineItemFromOrder(ok=ok, order=order)

