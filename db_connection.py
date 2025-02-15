import mysql.connector
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            print("Conexión exitosa a MySQL")
            return connection
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

if __name__ == "__main__":
    print("Ejecutando script...")
    connection = get_db_connection()
    if connection:
        print("Cerrando la conexión.")
        connection.close()
    else:
        print("No se pudo establecer la conexión.")