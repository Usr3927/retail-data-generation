import psycopg2
import random as rnd

class fact_orders_products:

    def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT,products,orders):
        self.DB_HOST=DB_HOST
        self.DB_NAME=DB_NAME
        self.DB_USER=DB_USER
        self.DB_PASS=DB_PASS
        self.DB_PORT=DB_PORT
        self.products=products
        self.orders=orders

    def run(self):
        rnd.seed(11)
        conn=psycopg2.connect(
            host=self.DB_HOST,
            database=self.DB_NAME,
            user=self.DB_USER,
            password=self.DB_PASS,
            port=self.DB_PORT
        )
        cur=conn.cursor()
        cur.execute(
            """
            DROP TABLE IF EXISTS fact_orders_products;
            """
        )
        conn.commit()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS fact_orders_products (
                id_order VARCHAR(50) NOT NULL,
                id_producto VARCHAR(50) NOT NULL,
                unidades INTEGER NOT NULL,
                peso NUMERIC(10, 3)
            );
            """
        )
        conn.commit()

        prodCategories=set([product[7] for product in self.products])
        for i in range(0, len(self.orders),1):
            productsVariable=[]
            productsNotVariable=[]
            products=[]
            for j in range(0,rnd.randrange(0,50,1),1):
                idCategory=rnd.randrange(0,len(prodCategories),1)
                category=[ elm for k,elm in enumerate(prodCategories) if k==idCategory][0]
                productsOfCategory=[product for product in self.products if category==product[7]]
                productBought=productsOfCategory[rnd.randrange(0,len(productsOfCategory),1)]
                if productBought[6]:
                    productsVariable.append(productBought[0])
                else:
                    productsNotVariable.append(productBought[0])
            
            productsNotVariable=set(productsNotVariable)
            for product in productsNotVariable:
                tmp=[self.orders[i][0],product,rnd.randrange(1,10,1),None]
                products.append(tmp)

            for product in productsVariable:
                tmp=[self.orders[i][0],product,1,rnd.random()*2.5+0.5]
                products.append(tmp)


            query=f"""
                    INSERT INTO fact_orders_products (
                        id_order, id_producto, unidades, peso
                    ) VALUES (
                        %s,%s,%s,%s
                    ); 
                """
            for order_product in products:
                cur.execute(query,(
                        order_product[0],order_product[1],order_product[2],order_product[3] 
                    )
                )
                if(i%100==0):
                    conn.commit()
        conn.commit()
        cur.close()
        conn.close()