# Shopify Internship Challenge
> Submission by Jordan Dearsley (SoftEng UWaterloo)

[Link to Challenge](https://docs.google.com/document/d/1YYDRf_CgQRryf5lZdkZ2o3Hm3erFSaISL1L1s8kLqsI/edit)

This project was built using Django and Django-graphene. I haven't used GraphQL before so please forgive any conventions best practices, etc. I haven't followed! I've tried my best to follow the provided documentation.

This project is live and deployed via Kubernetes as of this commit. Please see the [Demo](#demo) section to access it.

# Table of Contents
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Testing](#testing)
- [API](#api)
    - [Authentication](#authentication)
    - [Queries](#queries)
    - [Mutations](#mutations)
        - [Create](#create)
        - [Update](#update)
        - [Delete](#delete)
        - [Extra Functionality](#extra-functionality)

## Demo

This demo has been deployed to a Kubernetes Cluster and is accessible at [link](http:website.com).

The demo is login protected, and the credentials to access the GraphiQL dashboard are as follows:
```
Username: shopify

Password: pleasehireme
```

## Prerequisites

- Python 3.5+

## Installation and Setup

Clone the repo as-is, and in the root directory, run:
```
source env/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
If that doesn't work, try praying and/or doing a good deed before running again.

## API

This section is an overview of the available methods and queries created for this project. To learn more about the queries built in to GraphQL, check out the [GraphQL docs](https://graphql.org/learn/queries/).

### Authentication

This GraphiQL page is login protected. If the user is not authenticated and tries to access the `/graphql` endpoint, it redirects to `/login`.

To log out, hit the endpoint `/logout`

### Queries

The graphql query API is modelled as follows:

```graphql
shops: [Shop](
    id: ID!
    name: String!
    products: [Product]
    orders: [Order]
)

products: [Product](
    id: ID!
    name: String!
    value: Float!
    lineItems: [LineItem]
    lineitemmodelSet: [LineItem]
    shopmodelSet: [Shop]
)

orders: [Order](
    id: ID!
    buyer: String!
    lineItems: [LineItem]
    value: Float
    shopmodelSet: [Shop]
)

lineitems: [LineItem](
    id: ID!
    value: Float!
    quantity: Int!
    product: Product!
    productmodelSet: [Product]
    ordermodelSet: [Order]
)
```
An example query to pull all shops, with their products, orders, and associated line items looks like this:
```graphql
{
  shops {
    id
    name

    products {
      id
      name
      value

      lineItems{
        id
        quantity
        value
      } 
    }

    orders {
      id
      buyer
      value

      lineItems{
        id

        product{
          id
        }
        quantity
        value
      } 
    }
    
  }
}
```

### Mutations

#### Create
The following create mutations return the related model after creation, along with a variable `ok` that acts as a success flag for the query.

The integer arrays, ie. `products` in createShop, are an array of ids that map to the objects themselves. These can be added on creation, or afterwards via the [extra mutations](#extra-functionality).
```graphql
createShop(
    name: String
    orders: [Int]
    products: [Int]
): CreateShop

createProduct(
    lineItems: [Int]
    name: String
    value: Float
): CreateProduct

createOrder(
    buyer: String
    lineItems: [Int]
): CreateOrder

createLineItem(
    product: Int
    quantity: Int
): CreateLineItem
```
A few notes:

- The value of orders and line items are decided based on their respective parameters. 

- The value of an order is dependent on its line items and their values.

- The value of a line item is dependent on its quantity and the value of its product.

#### Update
These mutations update the values of the four model types, requiring the model's id. The rest of the fields are optional to change. If a field is not include, it will not be updated.

Updating an id list will overwrite the list with the given input. To simply add/remove from those lists, check out the [extra mutations](#extra-functionality).

The following update mutations return the related model after update, along with a variable `ok` that acts as a success flag for the query.

```graphql
updateShop(
    id: Int!
    name: String
    orders: [Int]
    products: [Int]
): UpdateShop

updateProduct(
    id: Int!
    lineItems: [Int]
    name: String
    value: Float
): UpdateProduct

updateOrder(
    buyer: String
    id: Int!
    lineItems: [Int]
): UpdateOrder

updateLineItem(
    id: Int!
    product: Int
    quantity: Int
): UpdateLineItem
```
A few notes:

- Updates to product value will update all associated line item values and order values.

- Updates to line item quantity or product will update its value and the value of any related orders.

- Updates to the line items of an order will update the order's value.

#### Delete
The following mutations take in the id of the model to be deleted. These functions return an `ok` success status flag
```graphql
deleteShop(id: Int!): DeleteShop
deleteProduct(id: Int!): DeleteProduct
deleteOrder(id: Int!): DeleteOrder
deleteLineItem(id: Int!): DeleteLineItem
```
A few notes:

- Any delete will remove any references to the object's id in the id arrays of other models attributes.

- Deleting a shop will delete all associated orders and products.

- Deleting a product will delete all associated line items, which will update the values of associated orders.

- Deleting an order will delete all associated line items.

- Deleting a line item will delete all references to it, and update the value of any orders containing it.

#### Extra Functionality

These mutations allow for the adding and removing of specific model ids in reference arrays. The names are self-explanatory, and they take in the ids of the related models. The model being changed will be returned, along with an `ok` status flag.

```graphql
addProductToShop(
    productId: Int!
    shopId: Int!
): AddProductToShop

addOrderToShop(
    orderId: Int!
    shopId: Int!
): AddOrderToShop

removeProductFromShop(
    productId: Int!
    shopId: Int!
): RemoveProductFromShop

removeOrderFromShop(
    orderId: Int!
    shopId: Int!
): RemoveOrderFromShop

addLineItemToProduct(
    lineItemId: Int!
    productId: Int!
): AddLineItemToProduct

addLineItemToOrder(
    lineItemId: Int!
    orderId: Int!
): AddLineItemToOrder

removeLineItemFromProduct(
    lineItemId: Int!
    productId: Int!
): RemoveLineItemFromProduct

removeLineItemFromOrder(
    lineItemId: Int!
    orderId: Int!
): RemoveLineItemFromOrder
```

A few notes:

- Adding/removing a line item to an order also updates its order value.
- Adding/removing does not delete the model it refers to, it only adds or removes the reference from the reffering model's list.

## Testing

A set of tests have been created that test all of the above queries and mutations. These tests can be run by using Django's built in test suite by running:
```
python manage.py test
```
In the root directory of the repo.
