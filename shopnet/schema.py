
import graphene
from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel
from graphene_django import converter, utils
from shopnet.mutations import line_item, order, product, shop

# READ queries
class Query(graphene.ObjectType):

    shops = graphene.List(shop.Shop)
    products = graphene.List(product.Product)
    orders = graphene.List(order.Order)
    lineitems = graphene.List(line_item.LineItem)

    def resolve_shops(self, info):
        return ShopModel.objects.all()

    def resolve_products(self, info):
        return ProductModel.objects.all()

    def resolve_orders(self, info):
        return OrderModel.objects.all()

    def resolve_lineitems(self, info):
        return LineItemModel.objects.all()

# All mutations
class MyMutations(graphene.ObjectType):

    create_shop = shop.CreateShop.Field()
    create_product = product.CreateProduct.Field()
    create_order = order.CreateOrder.Field()
    create_line_item = line_item.CreateLineItem.Field()

    update_shop = shop.UpdateShop.Field()
    update_product = product.UpdateProduct.Field()
    update_order = order.UpdateOrder.Field()
    update_line_item = line_item.UpdateLineItem.Field()

    delete_shop = shop.DeleteShop.Field()
    delete_product = product.DeleteProduct.Field()
    delete_order = order.DeleteOrder.Field()
    delete_line_item = line_item.DeleteLineItem.Field()

    add_product_to_shop = shop.AddProductToShop.Field()
    add_order_to_shop = shop.AddOrderToShop.Field()
    remove_product_from_shop = shop.RemoveProductFromShop.Field()
    remove_order_from_shop = shop.RemoveOrderFromShop.Field()

    add_line_item_to_product = product.AddLineItemToProduct.Field()
    add_line_item_to_order = order.AddLineItemToOrder.Field()
    remove_line_item_from_product = product.RemoveLineItemFromProduct.Field()
    remove_line_item_from_order = order.RemoveLineItemFromOrder.Field()

# The GraphQL Schema
schema = graphene.Schema(query=Query, mutation=MyMutations)

