from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.SportLine

# ENCAB_FACTURA
db.ENCAB_FACTURA.insert_one({
    "NUM_FACTURA": 1001,
    "ID_CLIENTE": 1,
    "FECHA_FAC": datetime.now(),
    "TOTAL": 150.00
})

# DETALLE_FACTURA
db.DETALLE_FACTURA.insert_one({
    "NUM_FACTURA": 1001,
    "COD_PRODUCTO": "P001",
    "CANTIDAD": 2
})

# CLIENTE
db.CLIENTE.insert_one({
    "ID_CLIENTE": 1,
    "NOMBRE": "John",
    "APELLIDO": "Doe",
    "CORREO": "john.doe@example.com"
})

# PRODUCTOS
db.PRODUCTOS.insert_one({
    "ID_PRODUCTOS": "P001",
    "PRECIO_VENTA": 50.00,
    "INVENTARIOS": 100
})

# PROVEEDOR
db.PROVEEDOR.insert_one({
    "COD_PROV": "PR001",
    "NOMBRE": "Proveedor A"
})

# ORDEN_COMPRA
db.ORDEN_COMPRA.insert_one({
    "NUM_OC": 2001,
    "COD_PROVEEDOR": "PR001",
    "FECHA_OC": datetime.now(),
    "APLICADA": False
})

# DETALLE_OC
db.DETALLE_OC.insert_one({
    "NUM_OC": 2001,
    "COD_PRODUCTO": "P001",
    "COSTO": 45.00,
    "CANTIDAD": 10
})

# USUARIO
db.USUARIO.insert_one({
    "ID": 1,
    "CLAVE": "password123",
    "TIPO": 1  # 1--ADM, 2--VENDEDOR
})
