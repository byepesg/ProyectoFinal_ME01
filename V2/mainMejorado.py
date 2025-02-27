import json
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

class Server:
    """Clase que representa un servidor con sus características clave"""
    
    def __init__(self, id, carga, latencia, disponibilidad, costo_migracion, riesgo):
        self.id = id
        self.carga = carga  # Carga actual del servidor (0 a 1)
        self.latencia = latencia  # Latencia en ms (0 a 1 normalizado)
        self.disponibilidad = disponibilidad  # Disponibilidad binaria (0 o 1)
        self.costo_migracion = costo_migracion  # Costo de mover una instancia a este servidor (0 a 1)
        self.riesgo = riesgo  # Nivel de aversión o preferencia al riesgo (-1 a 1)

    def calcular_utilidad(self, w1, w2, w3, w4):
        """Calcula la función de utilidad considerando actitud hacia el riesgo"""
        utilidad_base = (w1 * (1 - self.carga) +
                         w2 * (1 - self.costo_migracion) +
                         w3 * (1 - self.latencia) +
                         w4 * self.disponibilidad)

        # Ajuste según actitud hacia el riesgo
        if self.riesgo > 0:  
            return utilidad_base + (self.riesgo * random.uniform(0, 0.1))
        elif self.riesgo < 0:  
            return utilidad_base - (abs(self.riesgo) * random.uniform(0, 0.1))
        else:
            return utilidad_base

def seleccionar_mejor_servidor(servidores, w1, w2, w3, w4):
    """Selecciona el servidor con mayor utilidad esperada"""
    return max(servidores, key=lambda s: s.calcular_utilidad(w1, w2, w3, w4))

def generar_servidores(n):
    """Genera una lista de n servidores con valores aleatorios"""
    return [
        Server(
            id=i+1,
            carga=random.uniform(0, 1),
            latencia=random.uniform(0, 1),
            disponibilidad=random.choice([0, 1]),
            costo_migracion=random.uniform(0, 1),
            riesgo=random.uniform(-1, 1) 
        )
        for i in range(n)
    ]

def simular_escenarios(config):
    """Ejecuta simulaciones para múltiples escenarios y guarda resultados"""
    resultados = {}

    for escenario in config["escenarios"]:
        iteraciones = config["iteraciones"]
        n_servidores = config["n_servidores"]
        w1, w2, w3, w4 = escenario["pesos"]

        mejores_servidores = []
        for _ in range(iteraciones):
            servidores = generar_servidores(n_servidores)
            mejor = seleccionar_mejor_servidor(servidores, w1, w2, w3, w4)
            mejores_servidores.append(mejor.id)
        
        # Contar la frecuencia de selección de servidores
        conteo = dict(Counter(mejores_servidores))
        resultados[escenario["nombre"]] = conteo
    
    return resultados

def visualizar_resultados(resultados):
    """Grafica la frecuencia de selección de servidores para cada escenario"""
    for escenario, conteo in resultados.items():
        plt.figure(figsize=(8, 5))
        plt.bar(conteo.keys(), conteo.values(), color='blue', alpha=0.7)
        plt.xlabel("ID del Servidor")
        plt.ylabel("Frecuencia de Selección")
        plt.title(f"Distribución de Selección de Servidores - {escenario}")
        plt.xticks(list(conteo.keys()))
        plt.show()

def main():
    # Leer archivo de entrada
    with open("input.json", "r") as file:
        config = json.load(file)
    
    # Ejecutar simulaciones para diferentes escenarios
    resultados = simular_escenarios(config)
    
    # Guardar resultados en archivo de salida
    with open("output.json", "w") as file:
        json.dump(resultados, file, indent=4)
    
    # Visualizar resultados
    visualizar_resultados(resultados)

if __name__ == "__main__":
    main()
