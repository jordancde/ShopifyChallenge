from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel
import graphene
from graphene_django import DjangoObjectType

class Product(DjangoObjectType):
    class Meta:
        model = ProductModel

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        value = graphene.Float()
        line_items = graphene.List(graphene.Int, required=False)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: Product)

    def mutate(self, info, name, value, line_items=None):
        productModel = ProductModel.objects.create(name=name,value=value)

        # Adds all line items from array of ids
        if line_items:
            for l in line_items:
                productModel.line_items.add(LineItemModel.objects.get(pk=l))

        product = Product(
            name=productModel.name, 
            value=productModel.value,
            line_items=productModel.line_items.all(),
        )

        ok = True
        return CreateProduct(product=product, ok=ok)

# Update Product
class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        value = graphene.Float(required=False)
        line_items = graphene.List(graphene.Int,required=False)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: Product)

    def mutate(self, info, id, name=None, value=None, line_items=None):
        productModel = ProductModel.objects.get(id=id)
        
        if name:
            productModel.name = name

        # Clears line items and recreates with id list
        if line_items is not None:
            productModel.line_items.clear()
            
            for l in line_items:
                productModel.line_items.add(LineItemModel.objects.get(pk=l))
        
        if value:
            productModel.value = value
            productModel.save()

            # updates line items
            for line in productModel.line_items.all():
                line.recalculate_value()

                # updates related orders
                related_orders = OrderModel.objects.filter(line_items__in=[line])
                for order in related_orders:
                    order.recalculate_value()  
        
        productModel.save()

        product = Product(
            name=productModel.name,
            value=productModel.value,
            line_items=productModel.line_items.all()
        )

        ok = True
        return UpdateProduct(product=product, ok=ok)

# delete product - deletes associated line items
class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        productModel = ProductModel.objects.get(id=id)

        # Deletes related line items
        for line_item in productModel.line_items.all():
            line_id = line_item.pk

            # Gets list of orders that contain the line item
            related_orders = OrderModel.objects.filter(line_items__in=[line_id])

            # updates related orders
            for order in related_orders:
                order.line_items.remove(line_item)
                order.recalculate_value() 

            line_item.delete()

        productModel.delete()

        ok = True
        return DeleteProduct(ok=ok)


# Add line item to product
class AddLineItemToProduct(graphene.Mutation):
    class Arguments:
        line_item_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: Product)

    def mutate(self, info, line_item_id, product_id):
        lineItemModel = LineItemModel.objects.get(id=line_item_id)
        productModel = ProductModel.objects.get(id=product_id)

        productModel.line_items.add(lineItemModel)
        productModel.save()

        product = Product(
            id=productModel.id,
            name=productModel.name,
            value=productModel.value,
            line_items=productModel.line_items
        )

        ok = True
        return AddLineItemToProduct(ok=ok, product=product)

# Remove line item from product
class RemoveLineItemFromProduct(graphene.Mutation):
    class Arguments:
        line_item_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: Product)

    def mutate(self, info, line_item_id, product_id):
        lineItemModel = LineItemModel.objects.get(id=line_item_id)
        productModel = ProductModel.objects.get(id=product_id)

        productModel.line_items.remove(lineItemModel)
        productModel.save()

        product = Product(
            id=productModel.id,
            name=productModel.name,
            value=productModel.value,
            line_items=productModel.line_items
        )

        ok = True
        return AddLineItemToProduct(ok=ok, product=product)

