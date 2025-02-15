from locust import HttpUser, task, between

class BancoUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:5000"  # Usar la URL y puerto correctos del servidor Flask

    def on_start(self):
        """Método que se ejecuta cuando un usuario comienza la simulación."""
        # Verificar que la API está funcionando
        response = self.client.get("/")
        if response.status_code == 200:
            print("API funcionando correctamente")
        else:
            print(f"API no responde correctamente: {response.status_code}")

    @task
    def obtener_clientes(self):
        """Simula la solicitud GET para obtener todos los clientes."""
        response = self.client.get("/clientes")  # Asegúrate de que esta ruta sea correcta
        if response.status_code == 200:
            clientes = response.json()  # Obtener la respuesta JSON
            print(f"Se obtuvieron {len(clientes)} clientes.")
        else:
            print(f"Error al obtener clientes: {response.status_code}")

    @task
    def obtener_cliente_especifico(self):
        """Simula la solicitud GET para obtener un cliente específico (ID 2)."""
        cliente_id = 2  # Cliente con id_cliente 2
        response = self.client.get(f"/clientes/{cliente_id}")  # Cambiado aquí para buscar un cliente por ID
        if response.status_code == 200:
            cliente = response.json()  # Obtener la respuesta JSON
            print(f"Cliente con ID {cliente_id} encontrado: {cliente}")
        elif response.status_code == 404:
            print(f"Cliente con ID {cliente_id} no encontrado")
        else:
            print(f"Error al obtener cliente con ID {cliente_id}: {response.status_code}")
