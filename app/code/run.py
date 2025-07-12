from dim_products import dim_products
from dim_customers import dim_customers
from dim_shops import dim_shops
from fact_orders import fact_orders
from fact_orders_products import fact_orders_products

DB_HOST='retail-database'
DB_NAME='retail-data'
DB_USER='retail-data'
DB_PASS='1234'
DB_PORT='5432'

products=dim_products(DB_HOST,DB_NAME,DB_USER,DB_PASS,DB_PORT)
products.run()

shops=dim_shops(DB_HOST,DB_NAME,DB_USER,DB_PASS,DB_PORT,10)
shops.run()

customers=dim_customers(DB_HOST,DB_NAME,DB_USER,DB_PASS,DB_PORT, shops.data)
customers.run()

orders=fact_orders(DB_HOST,DB_NAME,DB_USER,DB_PASS,DB_PORT,customers.data, shops.data)
orders.run()

ordersProducts=fact_orders_products(DB_HOST,DB_NAME,DB_USER,DB_PASS,DB_PORT,products.data, orders.data)
ordersProducts.run()