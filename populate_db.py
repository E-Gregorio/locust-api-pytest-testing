from faker import Faker
import random
from db_connection import conectar  # Cambiado de 'conectar' a 'get_db_connection'

fake = Faker()

def insertar_clientes(n):
    conn = conectar()  # Cambiado aquí también
    cursor = conn.cursor()

    for _ in range(n):
        nombre = fake.name()
        direccion = fake.address()
        email = fake.unique.email()
        telefono = fake.phone_number()

        cursor.execute("INSERT INTO clientes (nombre, direccion, email, telefono) VALUES (%s, %s, %s, %s)", 
                       (nombre, direccion, email, telefono))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Se insertaron {n} clientes.")

def insertar_cuentas(n):
    conn = conectar()  # Cambiado aquí también
    cursor = conn.cursor()

    cursor.execute("SELECT id_cliente FROM clientes")
    clientes = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        id_cliente = random.choice(clientes)
        saldo = round(random.uniform(100, 5000), 2)
        tipo_cuenta = random.choice(["ahorro", "corriente"])

        cursor.execute("INSERT INTO cuentas (id_cliente, saldo, tipo_cuenta) VALUES (%s, %s, %s)", 
                       (id_cliente, saldo, tipo_cuenta))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Se insertaron {n} cuentas.")

def insertar_transacciones(n):
    conn = conectar()  # Cambiado aquí también
    cursor = conn.cursor()

    cursor.execute("SELECT id_cuenta FROM cuentas")
    cuentas = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        id_origen, id_destino = random.sample(cuentas, 2)
        monto = round(random.uniform(10, 1000), 2)

        cursor.execute("INSERT INTO transacciones (id_cuenta_origen, id_cuenta_destino, monto) VALUES (%s, %s, %s)", 
                       (id_origen, id_destino, monto))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Se insertaron {n} transacciones.")

# Ejecutar las inserciones
insertar_clientes(10)
insertar_cuentas(20)
insertar_transacciones(30)