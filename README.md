# 📘 Guía para Configurar y Probar la API Bancaria

Este documento te guiará a través del proceso de configuración, generación de datos, creación de una API con Flask, pruebas de carga con Locust, generación de reportes con Allure y la integración de un pipeline CI/CD con GitHub Actions.

---

## 🔥 Resumen del Flujo

✅ **1. Configuración del entorno** → Instalar dependencias y crear estructura del proyecto.  
✅ **2. Generación de datos aleatorios con Faker** → Poblamos MySQL con datos ficticios.  
✅ **3. Creación de una API con Flask** → Endpoints ficticios para simulación bancaria.  
✅ **4. Pruebas de carga con Locust** → Simular transacciones bancarias.  
✅ **5. Reportes con Allure** → Analizar resultados de rendimiento.  
✅ **6. CI/CD con GitHub Actions** → Automatizar pruebas en el pipeline.  

---

## 1️⃣ Configuración del Entorno

1. Clona el repositorio del proyecto:
   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto
   ```

2. Crea un entorno virtual e instala dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 2️⃣ Generación de Datos Aleatorios con Faker

Para poblar nuestra base de datos MySQL con datos ficticios, usamos **Faker**.

1. Instala la librería Faker si no lo has hecho:
   ```bash
   pip install faker
   ```

2. Crea un script `populate_db.py` para generar datos:
   ```python
   from faker import Faker
   import mysql.connector

   fake = Faker()

   conn = mysql.connector.connect(host='localhost', user='root', password='tu_clave', database='banco')
   cursor = conn.cursor()

   for _ in range(100):
       nombre = fake.name()
       email = fake.email()
       cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre, email))

   conn.commit()
   conn.close()
   ```

3. Ejecuta el script para poblar la base de datos:
   ```bash
   python populate_db.py
   ```

---

## 3️⃣ Creación de una API con Flask

1. Instala Flask:
   ```bash
   pip install flask
   ```

2. Crea un archivo `app.py` con la API:
   ```python
   from flask import Flask, jsonify

   app = Flask(__name__)

   @app.route('/clientes', methods=['GET'])
   def obtener_clientes():
       return jsonify({"mensaje": "Lista de clientes"})

   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. Ejecuta la API:
   ```bash
   python app.py
   ```

---

## 4️⃣ Pruebas de Carga con Locust

1. Instala Locust:
   ```bash
   pip install locust
   ```

2. Crea un archivo `locustfile.py`:
   ```python
   from locust import HttpUser, task

   class BancoUser(HttpUser):
       @task
       def obtener_clientes(self):
           self.client.get("/clientes")
   ```

3. Ejecuta Locust:
   ```bash
   locust -f locustfile.py --host=http://127.0.0.1:5000
   ```

4. Accede a la interfaz web de Locust en:
   ```
   http://127.0.0.1:8089

5. Ejecutando las pruebas de Locust

Paso 1: Navegar al directorio del proyecto

cd /ruta/a/tu/proyecto

Paso 2: Verificar si el puerto 8089 está en uso

netstat -ano | findstr :8089

Si el puerto está en uso, detén el proceso antes de continuar.

Paso 3: Detener procesos utilizando el puerto 8089

taskkill /PID <PID> /F

Paso 4: Ejecutar Locust

locust -f locustfile.py --host=http://127.0.0.1:5000

Paso 5: Acceder a la interfaz web de Locust

Abre tu navegador y accede a:

http://127.0.0.1:8089

Paso 6: Detener las pruebas

Presiona Ctrl+C en la terminal.
   ```

---

## 5️⃣ Reportes con Allure

1. Instala Allure:
   ```bash
   pip install allure-pytest
   ```

2. Ejecuta las pruebas y genera el reporte:
   ```bash
   pytest --alluredir=reportes/
   ```

3. Visualiza el reporte:
   ```bash
   allure serve reportes/
   ```

---

## 6️⃣ CI/CD con GitHub Actions

Para automatizar la ejecución de las pruebas en cada push, crea un archivo `.github/workflows/tests.yml`:

```yaml
name: CI/CD

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout del código
      uses: actions/checkout@v2

    - name: Configurar Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Ejecutar pruebas
      run: |
        pytest --alluredir=reportes/

    - name: Generar Reporte
      run: |
        allure generate reportes/ -o reportes/html --clean
```

---

✅ **Con esto, has configurado, probado y automatizado la API de tu proyecto bancario. ¡Felicidades!** 🚀

