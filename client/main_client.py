import socket
import time
import numpy as np
import sys

# Configuración de simulación
mean_delay = 3  # Media para simulación del tráfico (segundos)
std_dev_delay = 0.5  # Desviación estándar para simulación del tráfico (segundos)
windowC = 1.5 * mean_delay

#0 el buffer esta lleno
#1Hay espacio en el buffer

def send_file(server_ip, file_name):
    try:
        global windowC
        enviado = False
        intentos = 3
        while(not enviado and intentos > 0):
            print(f"Ventana : {windowC}")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, 9999))  # Asume el puerto 9999 como predeterminado
            
            #Respuesta inicial del servidor
            initial_r = client.recv(1024).decode()
            print(f"Respuesta inicial: {initial_r}")
            accion = int(initial_r)
            
            #Evalua disponibilidad del buffer
            if accion:
                # Medir tiempo real
                start_time = time.time()
                # Enviar archivo
                with open(file_name, "rb") as f:
                    client.sendfile(f)
                # Recibir respuesta del servidor
                response = client.recv(1024).decode()
                end_time = time.time()
                response_time = end_time - start_time
                # Simular retardo
                simulated_delay = np.random.normal(mean_delay, std_dev_delay,1)[0]
                total_time = response_time + simulated_delay
                print(f"Tiempo total: {total_time:.4f}")
                if total_time < windowC:
                    print(f"Respuesta del servidor: {response}.")
                    windowC = response_time + 1.1*simulated_delay
                    enviado = True
                else:
                    print(f"Tiempo de espera agotado...")
                    windowC = 1.5 * mean_delay
                    print(f"Reenviando el paquete {file_name}...\n")
            else:
                #Espera un periodo de tiempo para intentar el reenvío
                waiting_time = np.random.normal(mean_delay/2, std_dev_delay, 1)
                print("Esperando para reenvio...")
                time.sleep(int(waiting_time[0]))
                print(f"Reenviando el paquete {file_name}...\n")
                intentos -= 1
            client.close()
        if intentos <= 0:
            print("(500) Internal Server Error :(")
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
            print("---------------------------------------------------------------")
            file_name = input("Ingrese el nombre del archivo a enviar (o 'salir' para terminar): ").strip()
            if file_name.lower() == "salir":
                print("Terminando el programa.")
                break
            send_file(server_ip, file_name)
            another = input("¿Desea enviar otro archivo? (s/n): ").strip().lower()
            if another != "s":
                print("Terminando el programa.")
                break
            print("---------------------------------------------------------------\n")