tablesCreation=[
    """
    CREATE TABLE IF NOT EXISTS dim_tiendas (
        id_tienda VARCHAR(5) PRIMARY KEY,
        nombre_tienda VARCHAR(50) NOT NULL,
        ciudad_tienda VARCHAR(50) NOT NULL,
        provincia_tienda VARCHAR(50) NOT NULL,
        latitud_tienda DOUBLE PRECISION NOT NULL,
        longitud_tienda DOUBLE PRECISION NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS dim_productos (
        id_producto VARCHAR(8) PRIMARY KEY,
        nombre_producto VARCHAR(50) NOT NULL,
        precio_producto NUMERIC(10, 2) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS dim_clientes (
        id_cliente VARCHAR(8) PRIMARY KEY,
        nombre_cliente VARCHAR(50) NOT NULL,
        apellido_1_cliente VARCHAR(50) NOT NULL,
        apellido_2_cliente VARCHAR(50) NOT NULL,
        ciudad_cliente VARCHAR(50) NOT NULL,
        provincia_cliente VARCHAR(50) NOT NULL,
        nif_cliente VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS fact_orders (
        id_order VARCHAR(9) PRIMARY KEY,
        id_cliente VARCHAR(8) NOT NULL,
        fecha_order date NOT NULL,
        hora_order time NOT NULL,
        id_tienda VARCHAR(5) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS fact_orders_products (
        id_order VARCHAR(9) NOT NULL,
        id_product VARCHAR(8) NOT NULL,
        unidades INTEGER,
        peso DOUBLE PRECISION,
        volumen DOUBLE PRECISION
    );
    """
]