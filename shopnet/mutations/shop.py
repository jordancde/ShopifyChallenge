from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel
import graphene
from graphene_django import DjangoObjectType

class Shop(DjangoObjectType):
    class Meta:
        model = ShopModel

class CreateShop(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        products = graphene.List(graphene.Int,required=False)
        orders = graphene.List(graphene.Int, required=False)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, name, products=None, orders=None):
        shopModel = ShopModel.objects.create(name=name)

        # Adds products in param to shop product list
        if products is not None:
            for p in products:
                shopModel.products.add(ProductModel.objects.get(pk=p))

        # Adds orders in param to shop order list
        if orders is not None:
            for o in orders:
                shopModel.orders.add(OrderModel.objects.get(pk=p))
        
        shop = Shop(
            name=name, 
            products=shopModel.products.all(),
            orders=shopModel.orders.all(),
        )
        ok = True
        return CreateShop(shop=shop, ok=ok)

class UpdateShop(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        products = graphene.List(graphene.Int,required=False)
        orders = graphene.List(graphene.Int, required=False)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, id, name=None, products=None, orders=None):

        shopModel = ShopModel.objects.get(id=id)
        if name:
            shopModel.name = name

        # Clears the product list, then recreates with the new input
        if products is not None:
            shopModel.products.clear()
            
            for p in products:
                shopModel.products.add(ProductModel.objects.get(pk=p))

        # Clears the order list, then recreates with the new input
        if orders is not None:
            shopModel.orders.clear()
            for o in orders:
                shopModel.orders.add(OrderModel.objects.get(pk=p))
        
        shopModel.save()

        shop = Shop(
            name=name, 
            products=shopModel.products.all(),
            orders=shopModel.orders.all(),
        )

        ok = True
        return UpdateShop(shop=shop, ok=ok)

# delete shop - deletes products, orders, and their line items
class DeleteShop(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        shopModel = ShopModel.objects.get(id=id)

        # Deletes all products and line items
        for product in shopModel.products.all():
            for line_item in product.line_items.all():
                line_item.delete()
            product.delete()
        
        # Deletes all orders and line items
        for order in shopModel.orders.all():
            for line_item in order.line_items.all():
                line_item.delete()
            order.delete()

        shopModel.delete()

        ok = True
        return DeleteShop(ok=ok)

# EXTRAS
# Add product to shop list
class AddProductToShop(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        shop_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, shop_id, product_id):
        shopModel = ShopModel.objects.get(id=shop_id)
        productModel = ProductModel.objects.get(id=product_id)

        shopModel.products.add(productModel)
        shopModel.save()

        shop = Shop(
            id=shopModel.id,
            name=shopModel.name,
            products=shopModel.products,
            orders=shopModel.orders
        )

        ok = True
        return AddProductToShop(ok=ok, shop=shop)

# remove product from shop list
class RemoveProductFromShop(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        shop_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, shop_id, product_id):
        shopModel = ShopModel.objects.get(id=shop_id)
        productModel = ProductModel.objects.get(id=product_id)

        shopModel.products.remove(productModel)
        shopModel.save()

        shop = Shop(
            id=shopModel.id,
            name=shopModel.name,
            products=shopModel.products,
            orders=shopModel.orders
        )

        ok = True
        return RemoveProductFromShop(ok=ok, shop=shop)

# Add order to shop list
class AddOrderToShop(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)
        shop_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, shop_id, order_id):
        shopModel = ShopModel.objects.get(id=shop_id)
        orderModel = OrderModel.objects.get(id=order_id)

        shopModel.orders.add(orderModel)
        shopModel.save()

        shop = Shop(
            id=shopModel.id,
            name=shopModel.name,
            products=shopModel.products,
            orders=shopModel.orders
        )

        ok = True
        return AddOrderToShop(ok=ok, shop=shop)

# remove order from shop list
class RemoveOrderFromShop(graphene.Mutation):
    class Arguments:
        order_id = graphene.Int(required=True)
        shop_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, shop_id, order_id):
        shopModel = ShopModel.objects.get(id=shop_id)
        orderModel = OrderModel.objects.get(id=order_id)

        shopModel.orders.remove(orderModel)
        shopModel.save()

        shop = Shop(
            id=shopModel.id,
            name=shopModel.name,
            products=shopModel.products,
            orders=shopModel.orders
        )

        ok = True
        return RemoveOrderFromShop(ok=ok, shop=shop)