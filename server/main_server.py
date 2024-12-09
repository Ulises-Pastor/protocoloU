import socket
import threading
import numpy as np
import time

# Configuración del buffer y simulación
buffer_size = 4
buffer_lock = threading.Lock()
mean_time = 20  # Media para simulación del tiempo
std_dev_time = 2.5  # Desviación estándar para simulación del tiempo

def handle_client(client_socket, addr):
    global buffer_size
    # Simulación de la recepción
    with buffer_lock:
        if buffer_size < 1: #Espera un pequeño tiempo a que se libere un espacio
            time.sleep(int(mean_time/4))
        if buffer_size > 0:
            buffer_size -= 1
            client_socket.send(b"1")
            print(f"Paquete de {addr} aceptado. ({buffer_size} disponibles)\n")
        else:
            client_socket.send(b"0")
            client_socket.close()
            print(f"Paquete de {addr} rechazado")
            return
    # Recibir archivo
    filename = f"archivo_recibido_{addr[1]}.jpg"
    with open(filename, "wb") as f:
            data = client_socket.recv(1024)
            if not data:
                print("Error: No se recibió ningún dato.")
                # Incrementar el buffer cuando no se recibió información
                with buffer_lock:
                    buffer_size += 1
                return
            f.write(data)
    # Simular tiempo de "envío a la capa de aplicación"
    simulated_time = np.random.normal(mean_time, std_dev_time, 1)
    response = f"Conexión recibida. Buffer actual: {buffer_size}"
    client_socket.send(response.encode())
    client_socket.close()
    #Inicia "envio a la capa de aplicación"
    time.sleep(int(simulated_time[0]))
    # Incrementar el buffer después del tiempo simulado
    with buffer_lock:
        buffer_size += 1
        print(f"Espacio del buffer liberado... ({buffer_size} disponibles)")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)    #Tamaño de cola de espera de solicitudes
    print("Servidor escuchando en el puerto 9999...")
    while True:
        client_socket, addr = server.accept()
        print(f"Conexión establecida con {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()