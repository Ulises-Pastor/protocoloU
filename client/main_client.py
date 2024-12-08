import socket
import time
import numpy as np
import sys

# Configuración de simulación
mean_delay = 1  # Media para simulación del tráfico (segundos)
std_dev_delay = 0.3  # Desviación estándar para simulación del tráfico (segundos)

def send_file(server_ip, file_name):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, 9999))  # Asume el puerto 9999 como predeterminado

        # Medir tiempo real
        start_time = time.time()

        # Enviar archivo
        with open(file_name, "rb") as f:
            client.sendfile(f)

        # Recibir respuesta del servidor
        response = client.recv(1024).decode()
        end_time = time.time()

        # Simular retardo
        simulated_delay = max(0, np.random.randn() * std_dev_delay + mean_delay)
        total_time = (end_time - start_time) + simulated_delay

        print(f"Respuesta del servidor: {response}")
        print(f"Tiempo total (real + simulado): {total_time:.2f} segundos")

        client.close()
    except FileNotFoundError:
        print(f"Error: El archivo '{file_name}' no existe.")
    except ConnectionError:
        print("Error: No se pudo conectar al servidor.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cliente.py <direccion_del_servidor>")
    else:
        server_ip = sys.argv[1]

        while True:
            file_name = input("Ingrese el nombre del archivo a enviar (o 'salir' para terminar): ").strip()

            if file_name.lower() == "salir":
                print("Terminando el programa.")
                break

            send_file(server_ip, file_name)

            another = input("¿Desea enviar otro archivo? (s/n): ").strip().lower()
            if another != "s":
                print("Terminando el programa.")
                break