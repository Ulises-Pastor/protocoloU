import socket
import threading
import numpy as np
import os
import time

# Configuración del buffer y simulación
buffer_size = 4
buffer_lock = threading.Lock()
mean_time = 2  # Media para simulación del tiempo (segundos)
std_dev_time = 0.5  # Desviación estándar para simulación del tiempo (segundos)

def handle_client(client_socket, addr):
    global buffer_size

    # Simulación de la recepción
    with buffer_lock:
        if buffer_size > 0:
            buffer_size -= 1
        else:
            client_socket.send(b"Buffer lleno. Intente mas tarde.") #client_socket.send("Buffer lleno. Intente más tarde.".encode("utf-8"))
            client_socket.close()
            return

    # Recibir archivo
    filename = f"archivo_recibido_{addr[1]}.jpg"
    with open(filename, "wb") as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)

    # Simular tiempo de "envío a la capa de aplicación"
    simulated_time = max(0, np.random.randn() * std_dev_time + mean_time)
    time.sleep(simulated_time)

    # Incrementar el buffer después del tiempo simulado
    with buffer_lock:
        buffer_size += 1

    # Enviar respuesta al cliente
    response = f"Conexión recibida. Buffer actual: {buffer_size}\n"
    client_socket.send(response.encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Servidor escuchando en el puerto 9999...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión establecida con {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()