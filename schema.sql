CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(50),
    direccion TEXT
);

CREATE TABLE IF NOT EXISTS cuentas (
    id_cuenta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    saldo DECIMAL(10,2),
    tipo_cuenta VARCHAR(20),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS transacciones (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_cuenta_origen INT,
    id_cuenta_destino INT,
    monto DECIMAL(10,2),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cuenta_origen) REFERENCES cuentas(id_cuenta),
    FOREIGN KEY (id_cuenta_destino) REFERENCES cuentas(id_cuenta)
);