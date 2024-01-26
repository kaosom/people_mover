import threading
import time
import random

N = 10  # Número de estaciones

# Variables y recursos compartidos
mutex = threading.Lock()
parada_solicitada = [False] * N
ocupacion_tren = [False] * N

# Funciones para operaciones en trenes
def arrancar_tren(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Tren {tren} arrancó.")

def detener_tren(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Tren {tren} detenido.")

def apertura_puertas_salida(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Puertas de salida del Tren {tren} abiertas.")

def cierre_puertas_salida(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Puertas de salida del Tren {tren} cerradas.")

def apertura_puertas_entrada(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Puertas de entrada del Tren {tren} abiertas.")

def cierre_puertas_entrada(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Puertas de entrada del Tren {tren} cerradas.")

# Funciones para operaciones en estaciones
def ocupacion_vagon(tren):
    time.sleep(random.uniform(1, 3))
    return random.choice([True, False])

def lectura_anden(estacion):
    time.sleep(random.uniform(1, 3))
    print(f"Llamada desde la Estación {estacion} detectada.")

def lectura_parada(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Petición de parada en la próxima estación para Tren {tren} detectada.")

def detector(tren):
    time.sleep(random.uniform(1, 3))
    print(f"Proximidad a una estación detectada para Tren {tren}.")

# Función principal para controlar el sistema
def controlador_central():
    while True:
        for tren in range(1, N+1):
            if ocupacion_vagon(tren):
                mutex.acquire()
                parada_solicitada[tren-1] = True
                mutex.release()

        for tren in range(1, N+1):
            mutex.acquire()
            if parada_solicitada[tren-1]:
                detener_tren(tren)
                lectura_parada(tren)
                apertura_puertas_salida(tren)
                cierre_puertas_salida(tren)
                parada_solicitada[tren-1] = False
            mutex.release()

        time.sleep(1)

# Crear hilos para cada tren, estación y controlador
trenes = [threading.Thread(target=detector, args=(i,)) for i in range(1, N+1)]
estaciones = [threading.Thread(target=lectura_anden, args=(i,)) for i in range(1, N+1)]
controlador = threading.Thread(target=controlador_central)

# Iniciar los hilos
for t in trenes + estaciones + [controlador]:
    t.start()

# Esperar a que todos los hilos terminen (en la práctica, el controlador se ejecutaría de forma continua)
for t in trenes + estaciones + [controlador]:
    t.join()
