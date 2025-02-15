Aquí tienes el `README.md` actualizado para tu proyecto:

```markdown
# Proyecto Banco - Configuración y Generación de Datos

## 1. Configuración del Entorno

### 1.1 Crear la Carpeta del Proyecto

Abrimos **CMD o PowerShell (fuera de VS Code)** y ejecutamos:

```sh
mkdir proyecto-banco
cd proyecto-banco
code .
```

Esto abrirá VS Code en la carpeta del proyecto.

### 1.2 Crear un Entorno Virtual

Ejecutamos en la terminal de **VS Code**:

```sh
python -m venv venv
```

Para activarlo:

- **Windows (CMD/PowerShell)**  
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux**  
  ```sh
  source venv/bin/activate
  ```

### 1.3 Instalar Dependencias Iniciales

```sh
pip install flask mysql-connector-python faker locust allure-pytest pytest
```

#### Explicación de paquetes:
- `flask` → Para crear la API.
- `mysql-connector-python` → Conectar con MySQL.
- `faker` → Generar datos aleatorios.
- `locust` → Pruebas de carga y rendimiento.
- `allure-pytest` → Reportes visuales de pruebas.
- `pytest` → Ejecutar tests automatizados.

### 1.4 Crear la Estructura del Proyecto

```sh
mkdir app tests
touch app/__init__.py app/database.py app/api.py tests/test_api.py
```

Estructura esperada:
```
proyecto-banco/
│── app/
│   ├── __init__.py
│   ├── database.py
│   ├── api.py
│── tests/
│   ├── test_api.py
│── venv/ (entorno virtual)
│── requirements.txt
│── .gitignore
```

### 1.5 Guardar Dependencias en `requirements.txt`

```sh
pip freeze > requirements.txt
```

## 2. Generación de Datos Aleatorios con Faker

### 2.1 Instalar Faker y MySQL Connector

Ejecutamos en la terminal:

```sh
pip install faker mysql-connector-python
```

### 2.2 Crear Conexión a MySQL

Creamos el archivo **`database.py`** con el siguiente contenido:

```python
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2722",
        database="bank"
    )
```

### 2.3 Verificar la Conexión a la Base de Datos

Ejecutamos el siguiente código en **`database.py`**:

```python
if __name__ == "__main__":  
    conn = conectar()
    if conn.is_connected():
        print("Conexión exitosa a la base de datos")
        conn.close()
```

Ejecutamos en la terminal:

```sh
python app/database.py
```

Si todo está correcto, debería mostrar:

```
Conexión exitosa a la base de datos
```

## 3. Crear la API con Flask

### 3.1 Crear el archivo `api.py`

En **`app/api.py`**, escribimos el siguiente código para configurar la API que gestionará las rutas de clientes:

```python
from flask import Flask, jsonify, request
from app.database import conectar

app = Flask(__name__)

@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

@app.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    if cliente:
        return jsonify(cliente)
    return jsonify({"error": "Cliente no encontrado"}), 404

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

@app.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Cliente eliminado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
```

### 3.2 Ejecutar la API

Para ejecutar la API, usa el siguiente comando:

```sh
python -m app.api
```

La API estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 3.3 Pruebas de la API

Una vez la API esté corriendo, podrás probar las rutas:

- **GET /clientes**: Obtiene todos los clientes.
- **GET /clientes/{id}**: Obtiene un cliente específico.
- **POST /clientes**: Agrega un cliente.
- **PUT /clientes/{id}**: Actualiza los datos de un cliente.
- **DELETE /clientes/{id}**: Elimina un cliente.

### 3.4 Pruebas con Locust

Puedes usar **Locust** para hacer pruebas de carga y rendimiento. Para ello, debes crear un archivo de prueba de carga como **`tests/test_api.py`** y luego ejecutar las pruebas con Locust:

```sh
locust -f tests/test_api.py
```

## 4. Ejecución de Pruebas

Puedes ejecutar los tests automatizados utilizando **pytest** con el siguiente comando:

```sh
pytest
```

Esto generará los reportes de pruebas y asegurará que tu API esté funcionando correctamente.

---

✅ **¡Con esto has configurado y probado correctamente la API de tu proyecto Banco!** 🚀
```

Este `README.md` ahora cubre la configuración de todo el proyecto, desde la creación del entorno virtual hasta la ejecución de pruebas con **Locust** y **pytest**.

Aquí tienes el archivo `README.md` actualizado con los pasos y los comandos correctos para ejecutar las pruebas de **Locust**:

```markdown
# Guía para ejecutar las pruebas de Locust

Este proyecto utiliza **Locust** para realizar pruebas de carga en una API. A continuación se detallan los pasos y comandos necesarios para ejecutar las pruebas.

## Requisitos previos

1. Asegúrate de tener **Python** y **Locust** instalados en tu entorno de desarrollo.

   - Para instalar Locust, ejecuta el siguiente comando:
   
     ```bash
     pip install locust
     ```

2. Asegúrate de tener el servidor de la API que deseas probar en funcionamiento y accesible. En este ejemplo, se utiliza `http://127.0.0.1:5000` como la URL del servidor.

## Ejecutando las pruebas de Locust

Sigue estos pasos para ejecutar las pruebas de carga:

### Paso 1: Navegar al directorio del proyecto

Abre la terminal y navega al directorio donde se encuentra tu archivo `locustfile.py`:

```bash
cd /ruta/a/tu/proyecto
```

### Paso 2: Verificar si el puerto 8089 está en uso

Antes de ejecutar las pruebas, es importante asegurarse de que el puerto `8089` no esté siendo utilizado por otro proceso.

Ejecuta el siguiente comando para verificar si hay procesos utilizando el puerto `8089`:

```bash
netstat -ano | findstr :8089
```

Si encuentras un proceso en ejecución, necesitarás detenerlo antes de continuar. A continuación te explico cómo hacerlo.

### Paso 3: Detener procesos utilizando el puerto 8089

Si el puerto 8089 está en uso, sigue estos pasos para matar el proceso:

1. Encuentra el **PID** (ID de proceso) del servicio que está usando el puerto 8089.

   ```bash
   netstat -ano | findstr :8089
   ```

2. Una vez que hayas encontrado el PID del proceso, usa el siguiente comando para terminarlo:

   ```bash
   taskkill /PID <PID> /F
   ```

   Reemplaza `<PID>` con el número de ID del proceso.

3. Verifica nuevamente que el puerto esté libre:

   ```bash
   netstat -ano | findstr :8089
   ```

   Si no ves ninguna entrada, eso significa que el puerto está libre y puedes continuar.

### Paso 4: Ejecutar Locust

Para ejecutar las pruebas de carga con **Locust**, utiliza el siguiente comando:

```bash
locust -f locustfile.py --host=http://127.0.0.1:5000
```

- `-f locustfile.py`: Especifica el archivo de pruebas de Locust.
- `--host=http://127.0.0.1:5000`: Define la URL base de la API que deseas probar.

### Paso 5: Acceder a la interfaz web de Locust

Una vez que el servidor de Locust esté en ejecución, abre tu navegador y accede a la siguiente URL para iniciar las pruebas de carga:

```
http://127.0.0.1:8089
```

En la interfaz web de Locust, podrás configurar la cantidad de usuarios virtuales (clientes) y la tasa de solicitudes por segundo (RPS) que deseas simular.

### Paso 6: Detener las pruebas

Una vez que hayas terminado de ejecutar las pruebas, puedes detenerlas presionando **Ctrl+C** en la terminal.

### Comandos adicionales

- **Verificar el puerto 8089 en uso**:

   ```bash
   netstat -ano | findstr :8089
   ```

- **Matar un proceso utilizando el PID**:

   ```bash
   taskkill /PID <PID> /F
   ```

- **Detener las pruebas de Locust**:

   Presiona **Ctrl+C** en la terminal para detener el servidor de Locust.

---

Con estos pasos, deberías poder ejecutar tus pruebas de carga usando Locust sin problemas. Si tienes alguna duda o encuentras algún error durante el proceso, no dudes en contactarme para asistencia adicional.
```

Este README cubre los pasos completos para ejecutar Locust, desde la instalación hasta la ejecución y finalización de las pruebas. También incluye la parte relacionada con el manejo del puerto y la detención de procesos en conflicto.

Aquí tienes un resumen de los comandos que he usado en la terminal:

1. **Verificar si el puerto 8089 está en uso**:

   ```bash
   netstat -ano | findstr :8089
   ```

2. **Matar un proceso que está utilizando el puerto 8089** (reemplaza `<PID>` con el ID del proceso):

   ```bash
   taskkill /PID <PID> /F
   ```

3. **Ejecutar las pruebas de Locust** (reemplaza la URL según tu servidor y archivo de pruebas):

   ```bash
   locust -f locustfile.py --host=http://127.0.0.1:5000
   ```

4. **Acceder a la interfaz web de Locust** (en el navegador):

   ```
   http://127.0.0.1:8089
   ```

5. **Detener las pruebas de Locust**:

   Presiona **Ctrl+C** en la terminal.

Con estos comandos, podrás manejar el servidor de Locust y las pruebas de carga.