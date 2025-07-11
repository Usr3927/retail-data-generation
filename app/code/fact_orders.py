import psycopg2
import random as rnd
import datetime as dt

class fact_orders:

    def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT,customers,shops):
        self.DB_HOST=DB_HOST
        self.DB_NAME=DB_NAME
        self.DB_USER=DB_USER
        self.DB_PASS=DB_PASS
        self.DB_PORT=DB_PORT
        self.customers=customers
        self.shops=shops
        self.data=[]

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
            DROP TABLE IF EXISTS fact_orders;
            """
        )
        conn.commit()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS fact_orders (
                id_order VARCHAR(50) PRIMARY KEY,
                id_customer VARCHAR(50),
                fecha_order VARCHAR(50) NOT NULL,
                id_shop VARCHAR(50) NOT NULL
            );
            """
        )
        conn.commit()

        for i in range(0, 10*len(self.customers)):
            base_date=dt.datetime(2024,1,1,0,0)
            days=rnd.randint(0,30)
            hours=rnd.randint(10,21)
            minutes=rnd.randint(0,59)
            seconds=rnd.randint(0,59)
            
            delta=dt.timedelta(
                days=days,
                hours=hours,
                minutes=minutes,
                seconds=seconds
            )
            iCostumer=rnd.randrange(0,len(self.customers),1)
            tiendasCiudad=[ shop for shop in self.shops if shop[2]==self.customers[iCostumer][6]]
            tiendasCiudad=tiendasCiudad if len(tiendasCiudad)>0 and 0<rnd.randrange(0,100,1) else self.shops
            unknown=rnd.randrange(0,5,1)==0
            order=[
                ('000000000'+str(i))[-9:], 
                None if unknown else self.customers[iCostumer][0], 
                base_date+delta,
                self.shops[rnd.randrange(0,len(self.shops),1)][0] if unknown else tiendasCiudad[rnd.randrange(0,len(tiendasCiudad),1)][0]
            ]
            self.data.append(order)
            query=f"""
                    INSERT INTO fact_orders (
                        id_order, id_customer, fecha_order, id_shop
                    ) VALUES (
                        %s,%s,%s,%s
                    ); 
                """
            cur.execute(query,(
                    order[0],order[1],order[2],order[3] 
                )
            )
            if(i%100==0):
                conn.commit()
        conn.commit()
        cur.close()
        conn.close()