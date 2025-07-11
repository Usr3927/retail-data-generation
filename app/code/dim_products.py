import json 
import psycopg2

class dim_products:

    def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT):
        self.DB_HOST=DB_HOST
        self.DB_NAME=DB_NAME
        self.DB_USER=DB_USER
        self.DB_PASS=DB_PASS
        self.DB_PORT=DB_PORT
        self.data=[]

    def run(self):
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
            DROP TABLE IF EXISTS dim_productos;
            """
        )
        conn.commit()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS dim_productos (
                id_producto VARCHAR(50) PRIMARY KEY,
                nombre_marca VARCHAR(100),
                nombre_producto VARCHAR(200) NOT NULL,
                precio_producto NUMERIC(10, 2) NOT NULL,
                packaging VARCHAR(50) ,
                unit_name VARCHAR(50) ,
                peso_variable BOOLEAN NOT NULL,
                category VARCHAR(100)
            );
            """
        )
        conn.commit()
        for i in range(0,50,1):
            with open(f"/local/products_backup/products{("0"+str(i))[-2:]}.json") as file:
                data = json.load(file)
                for record in data:
                    query=f"""
                            INSERT INTO dim_productos (
                                id_producto, nombre_marca, nombre_producto, precio_producto, packaging, unit_name, peso_variable, category
                            ) VALUES (
                                %s,%s,%s,%s,%s,%s,%s,%s
                            ); 
                        """
                    self.data.append([record['id'],record['brand'],record['name'],record['price'],record['packaging'],record['unit_name'],record['is_variable_weight'],record['category']['name']])
                    cur.execute(query,(record['id'],record['brand'],record['name'],record['price'],record['packaging'],record['unit_name'],record['is_variable_weight'],record['category']['name']))
                conn.commit()
        conn.commit()
        cur.close()
        conn.close()
