import psycopg2
import random as rnd

class dim_customers:

    def __init__(self, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, shops):
        self.DB_HOST=DB_HOST
        self.DB_NAME=DB_NAME
        self.DB_USER=DB_USER
        self.DB_PASS=DB_PASS
        self.DB_PORT=DB_PORT
        self.shops=shops
        self.data=[]

    def run(self):
        rnd.seed(11)
        nombres_h = []
        nombres_m = []
        apellidos = []
        capitales = []
        letra_dni=["T","R","W","A","G","M","Y","F","P","D","X","B","N","J","Z","S","Q","V","H","L","C","K","E"]
        with open('/local/nombres_hombre.csv', 'r', encoding="utf-8") as file:
            for line in file:
                name=[
                    str(line.rstrip('\r\n').split(";")[0]),
                    int(line.rstrip('\r\n').split(";")[1])
                ]
                nombres_h.append(name)
        nombres_h=[[nombres_h[i][0], nombres_h[i][1], sum([nombres_h[j][1] for j in range(0,i,1)])] for i in range(0,len(nombres_h),1)]
        
        with open('/local/nombres_mujer.csv', 'r', encoding="utf-8") as file:
            for line in file:
                name=[
                    str(line.rstrip('\r\n').split(";")[0]),
                    int(line.rstrip('\r\n').split(";")[1])
                ]
                nombres_m.append(name)
        nombres_m=[[nombres_m[i][0], nombres_m[i][1], sum([nombres_m[j][1] for j in range(0,i,1)])] for i in range(0,len(nombres_m),1)]
        
        with open('/local/apellidos.csv', 'r', encoding="utf-8") as file:
            for line in file:
                name=[
                    str(line.rstrip('\r\n').split(";")[0]),
                    int(line.rstrip('\r\n').split(";")[1])
                ]
                apellidos.append(name)
        apellidos=[[apellidos[i][0], apellidos[i][1], sum([apellidos[j][1] for j in range(0,i,1)])] for i in range(0,len(apellidos),1)]

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
            DROP TABLE IF EXISTS dim_clientes;
            """
        )
        conn.commit()        
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS dim_clientes (
                id_cliente VARCHAR(50) PRIMARY KEY,
                sexo VARCHAR(1),
                nombre_cliente VARCHAR(50),
                apellido_1_cliente VARCHAR(50),
                apellido_2_cliente VARCHAR(50),
                dni_cliente VARCHAR(50),
                provincia_cliente VARCHAR(50),
                ciudad_cliente VARCHAR(50)
            );
            """
        )
        conn.commit()
        
        for i in range(0,1000*len(self.shops),1):
            query=f"""
                    INSERT INTO dim_clientes (
                        id_cliente, sexo, nombre_cliente, apellido_1_cliente, apellido_2_cliente, dni_cliente, provincia_cliente, ciudad_cliente
                    ) VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s
                    ); 
                """
            dni=i*10+rnd.randrange(0,10,1)+rnd.randrange(0,10,1)*10000000
            city=rnd.randrange(0,len(self.shops),1)
            sexo= "H" if rnd.randrange(0,2,1)==0 else "M"
            iNombreH=rnd.randrange(0,sum([nombres_h[i][1] for i in range(0,len(nombres_h),1)]),1)
            iNombreM=rnd.randrange(0,sum([nombres_m[i][1] for i in range(0,len(nombres_m),1)]),1)
            iApellido1=rnd.randrange(0,sum([apellidos[i][1] for i in range(0,len(apellidos),1)]),1)
            iApellido2=rnd.randrange(0,sum([apellidos[i][1] for i in range(0,len(apellidos),1)]),1)
            nombreH=[name[0] for name in nombres_h if name[2]<=iNombreH and name[2]+name[1]>iNombreH][0]
            nombreM=[name[0] for name in nombres_m if name[2]<=iNombreM and name[2]+name[1]>iNombreM][0]
            self.data.append(
                [
                    ("000000"+str(i))[-6:],
                    sexo,
                    nombreH if sexo=="H" else nombreM,
                    [apellido[0] for apellido in apellidos if apellido[2]<=iApellido1 and apellido[2]+apellido[1]>iApellido1][0],
                    [apellido[0] for apellido in apellidos if apellido[2]<=iApellido2 and apellido[2]+apellido[1]>iApellido2][0],
                    ("00000000"+str(dni))[-8:]+letra_dni[dni%23],
                    self.shops[city][3],
                    self.shops[city][2]
                ]
            )
            cur.execute(query,
                (
                    ("000000"+str(i))[-6:],
                    sexo,
                    nombreH if sexo=="H" else nombreM,
                    [apellido[0] for apellido in apellidos if apellido[2]<=iApellido1 and apellido[2]+apellido[1]>iApellido1][0],
                    [apellido[0] for apellido in apellidos if apellido[2]<=iApellido2 and apellido[2]+apellido[1]>iApellido2][0],
                    ("00000000"+str(dni))[-8:]+letra_dni[dni%23],
                    self.shops[city][3],
                    self.shops[city][2]
                )
            )
            if(i%100==0):
                conn.commit()
        conn.commit()
        cur.close()
        conn.close()