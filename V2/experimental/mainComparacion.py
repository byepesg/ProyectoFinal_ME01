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

def generar_valor_con_distribucion(distribucion, **kwargs):
    """Genera un valor basado en la distribución seleccionada"""
    if distribucion == "uniform":
        return random.uniform(0.2, 0.8)  # Evita valores extremos 0 y 1
    elif distribucion == "normal":
        mu = kwargs.get("mu", 0.5)
        sigma = kwargs.get("sigma", 0.10)  # Menos dispersión para evitar servidores extremadamente diferentes
        return max(0.1, min(0.9, random.gauss(mu, sigma)))  # Evita valores extremos
    elif distribucion == "exponential":
        lambda_ = kwargs.get("lambda_", 0.8)  # Reduce sesgo hacia valores muy bajos
        return min(1, max(0.2, random.expovariate(lambda_)))  # Valores dentro de un rango razonable
    elif distribucion == "beta":
        alpha = kwargs.get("alpha", 4)  # Más equilibrio hacia el centro (0.5)
        beta = kwargs.get("beta", 4)
        return random.betavariate(alpha, beta)
    else:
        raise ValueError(f"Distribución '{distribucion}' no reconocida.")

def generar_servidores(n, distribucion="beta"):
    """Genera una lista de n servidores con valores más balanceados"""
    return [
        Server(
            id=i+1,
            carga=generar_valor_con_distribucion(distribucion, alpha=3, beta=3),  # Más balance
            latencia=generar_valor_con_distribucion(distribucion, alpha=3, beta=3),
            disponibilidad=random.uniform(0.7, 1.0),  # Mayor disponibilidad media
            costo_migracion=generar_valor_con_distribucion(distribucion, alpha=3, beta=3),
            riesgo=random.uniform(-0.5, 0.5)  # Reduce la variabilidad extrema
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

def generar_diagrama_decision():
    """Genera un diagrama de decisión visual"""
    G = nx.DiGraph()

    # Agregar nodos de decisión
    G.add_node("Inicio")
    for i in range(1, 4):
        G.add_node(f"Servidor {i}")
        G.add_edge("Inicio", f"Servidor {i}", label=f"Opción {i}")
    
    # Agregar nodos de utilidad
    G.add_node("Decisión final")
    for i in range(1, 4):
        G.add_edge(f"Servidor {i}", "Decisión final", label="Evalúa Utilidad")
    
    # Dibujar el grafo
    plt.figure(figsize=(8, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, edge_color='gray')
    edge_labels = {(i, j): G.edges[i, j]['label'] for i, j in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Diagrama de Decisión para Selección de Servidores")
    plt.show()

def tomar_decisiones_secuenciales(n_pasos, n_servidores, w1, w2, w3, w4):
    """Simula un MDP donde los servidores ajustan su carga en cada iteración"""
    servidores = generar_servidores(n_servidores)

    for paso in range(n_pasos):
        mejor = seleccionar_mejor_servidor(servidores, w1, w2, w3, w4)
        print(f"Iteración {paso+1}: Servidor seleccionado -> {mejor.id}")

        # Simulación de ajuste de carga en servidores
        for server in servidores:
            server.carga = min(1, server.carga + random.uniform(-0.2, 0.2))  # Simula cambio de carga

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

    # Generar diagrama de decisión
    generar_diagrama_decision()

    # Simular decisiones secuenciales (MDP)
    print("\n--- Simulación de Decisiones Secuenciales ---")
    for escenario in config["escenarios"]:
        print(f"\nEscenario: {escenario['nombre']}")
        tomar_decisiones_secuenciales(5, config["n_servidores"], *escenario["pesos"])

if __name__ == "__main__":
    main()
