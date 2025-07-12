import psycopg2
import random as rnd

class dim_shops:

    def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, nShops):
        self.DB_HOST=DB_HOST
        self.DB_NAME=DB_NAME
        self.DB_USER=DB_USER
        self.DB_PASS=DB_PASS
        self.DB_PORT=DB_PORT
        self.nShops=nShops
        self.data=[]

    def run(self):
        rnd.seed(11)
        capitales = []

        with open('/local/población_capitales.txt', 'r', encoding="utf-8") as file:
            for line in file:
                capitales.append(line.rstrip('\r\n').split(";"))
            capitales.pop(0)
            capitales=[
                [
                    city[0],
                    city[1],
                    int(city[2].replace(".","")),
                    float(city[3].replace(",",".")),
                    float(city[4].replace(",","."))
                ] for city in capitales
            ]
            capitales=[
                [
                    capitales[i][0],
                    capitales[i][1],
                    capitales[i][2],
                    sum([capitales[j][2] for j in range(0,i,1)]),
                    sum([capitales[j][2] for j in range(0,i,1)])+capitales[i][2],
                    capitales[i][3],
                    capitales[i][4]
                ] for i in range(0,len(capitales),1)
            ]

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
            DROP TABLE IF EXISTS dim_tiendas;
            """
        )
        conn.commit()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS dim_tiendas (
                id_tienda VARCHAR(50) PRIMARY KEY,
                nombre_tienda VARCHAR(50),
                ciudad_tienda VARCHAR(50),
                provincia_tienda VARCHAR(50),
                latitud_tienda DOUBLE PRECISION,
                longitud_tienda DOUBLE PRECISION
            );
            """
        )
        conn.commit()
        
        for i in range(0,self.nShops,1):
            query=f"""
                    INSERT INTO dim_tiendas (
                        id_tienda, nombre_tienda, ciudad_tienda, provincia_tienda, latitud_tienda, longitud_tienda
                    ) VALUES (
                        %s,%s,%s,%s,%s,%s
                    ); 
                """
            city=rnd.randrange(0,sum([ capital[2] for capital in capitales]),1)
            
            self.data.append(
                [
                    ("0000"+str(i))[-4:],
                    "SHOP-"+("0000"+str(i))[-4:],
                    [ capital[0] for capital in capitales if capital[3]<=city and city<capital[4]][0],
                    [ capital[1] for capital in capitales if capital[3]<=city and city<capital[4]][0],
                    [ capital[5] for capital in capitales if capital[3]<=city and city<capital[4]][0]-0.045+0.09*rnd.random(),
                    [ capital[6] for capital in capitales if capital[3]<=city and city<capital[4]][0]-0.045+0.09*rnd.random()  
                ]
            )
            cur.execute(query,(
                    ("0000"+str(i))[-4:],
                    "SHOP-"+("0000"+str(i))[-4:],
                    [ capital[0] for capital in capitales if capital[3]<=city and city<capital[4]][0],
                    [ capital[1] for capital in capitales if capital[3]<=city and city<capital[4]][0],
                    [ capital[5] for capital in capitales if capital[3]<=city and city<capital[4]][0]-0.045+0.09*rnd.random(),
                    [ capital[6] for capital in capitales if capital[3]<=city and city<capital[4]][0]-0.045+0.09*rnd.random()    
                )
            )
            if(i%100==0):
                conn.commit()
        conn.commit()
        cur.close()
        conn.close()