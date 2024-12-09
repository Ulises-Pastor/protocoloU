import socket
import threading
import numpy as np
import os
import time

# Configuración del buffer y simulación
buffer_size = 4

buffer_lock = threading.Lock()
mean_time = 10  # Media para simulación del tiempo (segundos)
std_dev_time = 2.5  # Desviación estándar para simulación del tiempo (segundos)

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
            data = client_socket.recv(1024)
            if not data:
                print("Error: No se recibió ningún dato.")
                # Incrementar el buffer
                with buffer_lock:
                    buffer_size += 1
                return
            f.write(data)

    # Simular tiempo de "envío a la capa de aplicación"
    simulated_time = np.random.normal(mean_time, std_dev_time, 1)
    
    response = f"Conexión recibida. Buffer actual: {buffer_size}\n"
    client_socket.send(response.encode())
    client_socket.close()
    """El servidor recibe el archivo y lo guarda en el sistema de archivos local. Luego, envía una respuesta al cliente con el estado del buffer y cierra la conexión. El tiempo de simulación se calcula aleatoriamente y se envía al cliente como parte de la respuesta."""
    
    """desde aqui se simula el tiempo del procesamiendo dl buffer  
    |
    |
    V
    """
    time.sleep(int(simulated_time[0]))

    # Incrementar el buffer después del tiempo simulado
    with buffer_lock:
        buffer_size += 1
        print(f"Espacio del buffer liberado... ({buffer_size} disponibles)")

    # Enviar respuesta al cliente
    

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