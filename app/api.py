from flask import Flask, jsonify, request
from app.database import conectar



app = Flask(__name__)

# Ruta para la raíz del servidor
@app.route('/', methods=['GET'])
def home():
    return "API funcionando correctamente", 200

# Ruta para obtener todos los clientes
@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

# Ruta para obtener un cliente por id
@app.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    if cliente:
        return jsonify(cliente)
    return jsonify({"error": "Cliente no encontrado"}), 404

# Ruta para agregar un cliente
@app.route('/clientes', methods=['POST'])
def agregar_cliente():
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)"
    valores = (data['nombre'], data['email'], data['telefono'], data['direccion'])
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Cliente agregado correctamente"}), 201

# Ruta para actualizar un cliente
@app.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    data = request.json
    conn = conectar()
    cursor = conn.cursor()
    sql = "UPDATE clientes SET nombre=%s, email=%s, telefono=%s, direccion=%s WHERE id=%s"
    valores = (data['nombre'], data['email'], data['telefono'], data['direccion'], id)
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Cliente actualizado correctamente"})

# Ruta para eliminar un cliente
@app.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Cliente eliminado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
