from django.test import TestCase
from graphene.test import Client
from shopnet.schema import schema
from shopnet.models import ShopModel, ProductModel, OrderModel, LineItemModel


# Create your tests here.
class APITest(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_create_shop(self):
        executed = self.client.execute('''
            mutation CreateShop {
                createShop(name: "myshop") {
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
        shop = ShopModel.objects.get(name="myshop")
        self.assertEquals(shop.name,"myshop")
    
    def test_create_product(self):
        executed = self.client.execute('''
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
        product = ProductModel.objects.get(name="product")
        self.assertEquals(product.name,"product")

    def test_create_order(self):
        executed = self.client.execute('''
            mutation CreateOrder {
                createOrder(buyer: "john") {
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
        order = OrderModel.objects.get(buyer="john")
        self.assertEquals(order.buyer,"john")

    def test_create_line_item(self):

        self.test_create_product()

        executed = self.client.execute('''
            mutation CreateLineItem {
                createLineItem(product: 1, quantity: 3) {
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
        line_item = LineItemModel.objects.get(pk=1)
        self.assertEquals(line_item.value,60.00)

    def test_update_shop(self):
        self.test_create_shop()
        self.test_create_product()
        executed = self.client.execute('''
            mutation UpdateShop {
                updateShop(id: 2,name: "test", products: [3]) {
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
        shop = ShopModel.objects.get(pk=2)

        self.assertEquals(shop.name,"test")
        self.assertTrue(shop.products.all()[0].name,"product")

