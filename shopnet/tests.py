from django.test import TestCase
from graphene.test import Client
from shopnet.schema import schema
from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel


# Create your tests here.
class APITest(TestCase):
    def setUp(self):
        self.client = Client(schema)

        # create a product

        self.client.execute('''
            mutation CreateProduct {
                createProduct(name: "product", value: 20.00) {
                    product{
                        name
                        value
                        lineItems {
                            id
                        }
                    }
                    ok
                }
            }
        '''
        )

        self.product = ProductModel.objects.get(name="product")

        # create line item

        self.client.execute('''
            mutation CreateLineItem {
                createLineItem(product:'''+str(self.product.pk)+''', quantity: 3) {
                    lineItem {
                        product {
                            id
                        }
                        quantity
                        value
                    }
                    
                    ok
                }
            }
        '''
        )

        self.line_item = LineItemModel.objects.get(quantity=3)

        # create order

        self.client.execute('''
            mutation CreateOrder {
                createOrder(buyer: "john", lineItems: ['''+str(self.line_item.pk)+''']) {
                    order{
                        buyer
                        value
                        lineItems {
                            id
                        }
                    }
                    ok
                }
            }
        '''
        )

        self.order = OrderModel.objects.get(buyer="john")

        # create a shop

        self.client.execute('''
            mutation CreateShop {
                createShop(name: "myshop", products: ['''+str(self.product.pk)+'''],orders: ['''+str(self.order.pk)+''']) {
                    shop{
                        name
                        products {
                            id
                        }
                        orders {
                            id
                        }
                    }
                    ok
                }
            }
        '''
        )

        self.shop = ShopModel.objects.get(name="myshop")


    def test_create_shop(self):
        self.assertEquals(self.shop.name,"myshop")
    
    def test_create_product(self):
        self.assertEquals(self.product.name,"product")

    def test_create_order(self):
        self.assertEquals(self.order.buyer,"john")
        self.assertEquals(self.order.value,60.00)

    def test_create_line_item(self):
        self.assertEquals(self.line_item.value,60.00)

    def test_update_shop(self):
        executed = self.client.execute('''
            mutation UpdateShop {
                updateShop(id: '''+str(self.shop.pk)+''',name: "test", products: ['''+str(self.product.pk)+''']) {
                    shop{
                        name
                        products{
                            id
                        }
                    }
                    ok
                }

            }
        '''
        )
        self.shop.refresh_from_db()

        self.assertEquals(self.shop.name,"test")
        self.assertTrue(self.shop.products.all()[0].name,"product")
    
    # update in product value updates line item and order values
    def test_update_product(self):
        executed = self.client.execute('''
            mutation UpdateProduct {
                updateProduct(id: '''+str(self.product.pk)+''',value: 10) {
                    product{
                        name
                        value
                    }
                    ok
                }

            }
        '''
        )

        self.product.refresh_from_db()
        self.line_item.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEquals(self.product.value,10)
        self.assertEquals(self.line_item.value,30)
        self.assertEquals(self.order.value,30)

    def test_update_order(self):
        executed = self.client.execute('''
            mutation UpdateOrder {
                updateOrder(id: '''+str(self.order.pk)+''',buyer: "josh",lineItems:[]) {
                    order{
                        buyer
                        value
                        lineItems{
                            id
                        }
                    }
                    ok
                }
            }
        '''
        )

        self.order.refresh_from_db()
        self.assertEquals(self.order.value,0)
        self.assertEquals(self.order.buyer,"josh")
        
    def test_update_line_item(self):
        executed = self.client.execute('''
            mutation UpdateLineItem {
                updateLineItem(id: '''+str(self.line_item.pk)+''',quantity: 1) {
                    lineItem{
                        quantity
                        product {
                            id
                        }
                        value
                    }
                    ok
                }
            }
        '''
        )

        self.line_item.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEquals(self.line_item.value,20)
        self.assertEquals(self.order.value,20)

    def test_delete_shop(self):
        executed = self.client.execute('''
            mutation DeleteShop {
                deleteShop(id: '''+str(self.shop.pk)+''') {
                    ok
                }
            }
        '''
        )

        self.assertEquals(ShopModel.objects.all().count(),0)
        self.assertEquals(ProductModel.objects.all().count(),0)
        self.assertEquals(OrderModel.objects.all().count(),0)
        self.assertEquals(LineItemModel.objects.all().count(),0)

    def test_delete_product(self):
        executed = self.client.execute('''
            mutation DeleteProduct {
                deleteProduct(id: '''+str(self.product.pk)+''') {
                    ok
                }
            }
        '''
        )

        self.order.refresh_from_db()

        self.assertEquals(ShopModel.objects.all().count(),1)
        self.assertEquals(self.shop.products.all().count(),0)
        self.assertEquals(LineItemModel.objects.all().count(),0)
        self.assertEquals(self.order.value,0)
    
    def test_delete_order(self):
        executed = self.client.execute('''
            mutation DeleteOrder {
                deleteOrder(id: '''+str(self.order.pk)+''') {
                    ok
                }
            }
        '''
        )

        self.assertEquals(self.shop.orders.all().count(),0)
        self.assertEquals(LineItemModel.objects.all().count(),0)

    def test_delete_line_items(self):
        executed = self.client.execute('''
            mutation DeleteLineItems {
                deleteLineItem(id: '''+str(self.line_item.pk)+''') {
                    ok
                }
            }
        '''
        )

        self.order.refresh_from_db()

        self.assertEquals(self.order.value,0)
        self.assertEquals(LineItemModel.objects.all().count(),0)

    def test_delete_line_items(self):
        executed = self.client.execute('''
            mutation DeleteLineItems {
                deleteLineItem(id: '''+str(self.line_item.pk)+''') {
                    ok
                }
            }
        '''
        )

        self.order.refresh_from_db()

        self.assertEquals(self.order.value,0)
        self.assertEquals(LineItemModel.objects.all().count(),0)

    def test_remove_add_product_shop(self):
        executed = self.client.execute('''
            mutation RemoveProductFromShop {
                removeProductFromShop(shop_id: '''+str(self.shop.pk)+''',product_id: '''+str(self.product.pk)+''') {
                    shop{
                        name
                        products{
                            id
                        }
                    }
                    ok
                }
            }
        '''
        )
        # START HERE, find out why this isn't working
        self.shop.refresh_from_db()
        self.assertEquals(self.shop.products.all(),None)


