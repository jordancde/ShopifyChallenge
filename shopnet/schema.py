
from graphene_django import DjangoObjectType
import graphene
from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel
from graphene_django import converter, utils

class Shop(DjangoObjectType):

    class Meta:
        model = ShopModel


class Product(DjangoObjectType):
    class Meta:
        model = ProductModel

class Order(DjangoObjectType):
    class Meta:
        model = OrderModel

class LineItem(DjangoObjectType):
    class Meta:
        model = LineItemModel


class Query(graphene.ObjectType):

    shops = graphene.List(Shop)
    products = graphene.List(Product)
    orders = graphene.List(Order)
    lineitems = graphene.List(LineItem)

    def resolve_shops(self, info):
        return ShopModel.objects.all()

    def resolve_products(self, info):
        return ProductModel.objects.all()

    def resolve_orders(self, info):
        return OrderModel.objects.all()

    def resolve_lineitems(self, info):
        return LineItemModel.objects.all()

class CreateShop(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        products = graphene.List(graphene.Int,required=False)
        orders = graphene.List(graphene.Int, required=False)

    ok = graphene.Boolean()
    shop = graphene.Field(lambda: Shop)

    def mutate(self, info, name, products=None, orders=None):
        shopModel = ShopModel.objects.create(name=name)

        if products:
            for p in products:
                shopModel.products.add(ProductModel.objects.get(pk=p))

        if orders:
            for o in orders:
                shopModel.orders.add(OrderModel.objects.get(pk=p))
        
        shop = Shop(
            name=name, 
            products=shopModel.products.all(),
            orders=shopModel.orders.all(),
        )
        ok = True
        return CreateShop(shop=shop, ok=ok)

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        value = graphene.Float()
        line_items = graphene.List(graphene.Int, required=False)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: Product)

    def mutate(self, info, name, value, line_items=None):
        productModel = ProductModel.objects.create(name=name,value=value)

        if line_items:
            for l in line_items:
                productModel.line_items.add(LineItemModel.objects.get(pk=l))

        product = Product(
            name=name, 
            value=value,
            line_items=productModel.line_items.all(),
        )

        ok = True
        return CreateProduct(product=product, ok=ok)

class CreateOrder(graphene.Mutation):
    class Arguments:
        buyer = graphene.String()
        line_items = graphene.List(graphene.Int,required=False)

    ok = graphene.Boolean()
    order = graphene.Field(lambda: Order)

    def mutate(self, info, buyer, line_items=None):
        orderModel = OrderModel.objects.create(buyer=buyer)

        total_value = 0
        if line_items:
            for l in line_items:
                line_model = LineItemModel.objects.get(pk=l)
                total_value += line_model.value
                orderModel.line_items.add(line_model)

        orderModel.value = total_value
        orderModel.save()

        order = Order(
            value=orderModel.value,
            buyer=buyer, 
            line_items=orderModel.line_items.all()
        )

        ok = True
        return CreateOrder(order=order, ok=ok)

class CreateLineItem(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int()
        product = graphene.Int()

    ok = graphene.Boolean()
    line_item = graphene.Field(lambda: LineItem)

    def mutate(self, info, quantity, product):

        lineItemModel = LineItemModel.objects.create(
            quantity=quantity,
            product=ProductModel.objects.get(pk=product),
            value = quantity*ProductModel.objects.get(pk=product).value
        )
        
        line_item = LineItem(
            value=quantity*ProductModel.objects.get(pk=product).value,
            quantity=quantity,
            product=ProductModel.objects.get(pk=product)
        )

        ok = True
        return CreateLineItem(line_item=line_item, ok=ok)

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

        if products:
            shopModel.products.clear()
            
            for p in products:
                shopModel.products.add(ProductModel.objects.get(pk=p))

        if orders:
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

        if line_items:
            productModel.line_items.clear()
            
            for l in line_items:
                productModel.line_items.add(LineItemModel.objects.get(pk=p))

        if value:
            productModel.value = value
            for line in productModel.line_items.all():
                line.value = value*line.quantity
                line.save()
        
        productModel.save()

        product = Product(
            name=productModel.name,
            value=productModel.value,
            line_items=productModel.line_items.all()
        )

        ok = True
        return UpdateProduct(product=product, ok=ok)

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

        if line_items:
            orderModel.line_items.clear()
            
            for l in line_items:
                orderModel.line_items.add(LineItemModel.objects.get(pk=p))

            total_value = 0

            for l in line_items:
                line_model = LineItemModel.objects.get(pk=l)
                total_value += line_model.value

            orderModel.value = total_value


        orderModel.save()
        
        order = Order(
            buyer=productModel.name,
            value=productModel.value,
            line_items=productModel.line_items.all()
        )

        ok = True
        return UpdateOrder(order=order, ok=ok)

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

            lineItemModel.value = lineItemModel.quantity*lineItemModel.product.value
            lineItemModel.save()

            related_orders = OrderModel.objects.filter(line_items__id=id)
            
            for order in related_orders:
                total = 0
                for l in order.line_items:
                    total += l.value
                order.value = total
                order.save()

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

        related_orders = OrderModel.objects.filter(line_items__id=id)
            
        for order in related_orders:
            total = 0
            for l in order.line_items:
                total += l.value
            order.value = total
            order.save()

        lineItemModel.delete()

        ok = True
        return DeleteLineItem(ok=ok)

# delete order - deletes associated line items
class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        orderModel = OrderModel.objects.get(id=id)

        for line_item in orderModel.line_items:
            line_item.delete()

        orderModel.delete()

        ok = True
        return DeleteOrder(ok=ok)

# delete product - deletes associated line items
class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        productModel = ProductModel.objects.get(id=id)

        for line_item in productModel.line_items:
            line_item.delete()

        productModel.delete()

        ok = True
        return DeleteProduct(ok=ok)

# delete shop - deletes products, orders, and their line items

class DeleteShop(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        shopModel = ShopModel.objects.get(id=id)

        for product in shopModel.products:
            for line_item in product.line_items:
                line_item.delete()
            product.delete()
        
        for order in shopModel.orders:
            for line_item in order.line_items:
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

        total = 0
        for l in orderModel.line_items:
            total += l.value
        orderModel.value = total

        orderModel.save()

        order = Order(
            id=orderModel.id,
            buyer=orderModel.buyer,
            value=orderModel.value,
            line_items=orderModel.line_items
        )

        ok = True
        return AddLineItemToOrder(ok=ok, order=order)

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

        total = 0
        for l in orderModel.line_items:
            total += l.value
        orderModel.value = total

        orderModel.save()

        order = Order(
            id=orderModel.id,
            buyer=orderModel.buyer,
            value=orderModel.value,
            line_items=orderModel.line_items
        )

        ok = True
        return RemoveLineItemFromOrder(ok=ok, order=order)

# test removes to make sure they are removed from reference sets

class MyMutations(graphene.ObjectType):

    create_shop = CreateShop.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    create_line_item = CreateLineItem.Field()

    update_shop = UpdateShop.Field()
    update_product = UpdateProduct.Field()
    update_order = UpdateOrder.Field()
    update_line_item = UpdateLineItem.Field()

    delete_shop = DeleteShop.Field()
    delete_product = DeleteProduct.Field()
    delete_order = DeleteOrder.Field()
    delete_line_item = DeleteLineItem.Field()

    add_product_to_shop = AddProductToShop.Field()
    add_order_to_shop = AddOrderToShop.Field()
    remove_product_from_shop = RemoveProductFromShop.Field()
    remove_order_from_shop = RemoveOrderFromShop.Field()

    add_line_item_to_product = AddLineItemToProduct.Field()
    add_line_item_to_order = AddLineItemToOrder.Field()
    remove_line_item_from_product = RemoveLineItemFromProduct.Field()
    remove_line_item_from_order = RemoveLineItemFromOrder.Field()




schema = graphene.Schema(query=Query, mutation=MyMutations)

