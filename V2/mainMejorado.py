import json
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
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
        return random.uniform(0, 1)
    elif distribucion == "normal":
        mu = kwargs.get("mu", 0.5)
        sigma = kwargs.get("sigma", 0.15)
        return max(0, min(1, random.gauss(mu, sigma)))  # Recorte entre 0 y 1
    elif distribucion == "exponential":
        lambda_ = kwargs.get("lambda_", 1.5)
        return min(1, random.expovariate(lambda_))
    elif distribucion == "beta":
        alpha = kwargs.get("alpha", 2)
        beta = kwargs.get("beta", 5)
        return random.betavariate(alpha, beta)
    else:
        raise ValueError(f"Distribución '{distribucion}' no reconocida.")

def generar_servidores(n, distribucion="exponential"):
    """Genera una lista de n servidores con valores aleatorios según una distribución"""
    return [
        Server(
            id=i+1,
            carga=generar_valor_con_distribucion(distribucion),
            latencia=generar_valor_con_distribucion(distribucion),
            disponibilidad=random.choice([0, 1]),
            costo_migracion=generar_valor_con_distribucion(distribucion),
            riesgo=random.uniform(-1, 1)  # Siempre de -1 a 1
        )
        for i in range(n)
    ]

def simular_escenarios(config):
    """Ejecuta simulaciones para múltiples escenarios y guarda resultados"""
    resultados = {}

    for escenario in config["escenarios"]:
        iteraciones = config["iteraciones"]
        n_servidores = config["n_servidores"]

        pesos = escenario["pesos"]

        # Asegurar que hay al menos 4 pesos y rellenar si es necesario
        while len(pesos) < 4:
            pesos.append(0.1)  # Agregamos valores pequeños para compensar

        # Si hay más de 4, solo tomamos los primeros 4 para evitar el error
        pesos = pesos[:4]

        mejores_servidores = []
        for _ in range(iteraciones):
            servidores = generar_servidores(n_servidores)
            mejor = max(servidores, key=lambda s: s.calcular_utilidad(*pesos))
            mejores_servidores.append(mejor.id)

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

def tomar_decisiones_secuenciales(iteraciones, n_servidores, *pesos):
    """Simula la toma de decisiones con tres métodos: Utilidad, Round-Robin y Least Connections"""
    if len(pesos) < 4:
        raise ValueError("Se requieren al menos 4 pesos para la toma de decisiones.")
    
    # Tomamos solo 4 pesos
    pesos = pesos[:4]

    # Contadores de servidores seleccionados en cada método
    seleccion_utilidad = []
    seleccion_round_robin = []
    seleccion_least_connections = []

    # Generar servidores
    servidores = generar_servidores(n_servidores)

    # Inicializar estado de conexiones para Least Connections
    conexiones = {s.id: random.randint(1, 10) for s in servidores}

    for i in range(iteraciones):
        # Método de Utilidad
        mejor_utilidad = max(servidores, key=lambda s: s.calcular_utilidad(*pesos))
        seleccion_utilidad.append(mejor_utilidad.id)

        # Método Round-Robin
        mejor_round_robin = servidores[i % n_servidores]
        seleccion_round_robin.append(mejor_round_robin.id)

        # Método Least Connections
        mejor_least_connections = min(conexiones, key=conexiones.get)
        seleccion_least_connections.append(mejor_least_connections)
        conexiones[mejor_least_connections] += 1  # Incrementar carga

        print(f"Iteración {i+1}:")
        print(f"  - Método Utilidad -> Servidor {mejor_utilidad.id}")
        print(f"  - Método Round-Robin -> Servidor {mejor_round_robin.id}")
        print(f"  - Método Least Connections -> Servidor {mejor_least_connections}")

    # Devolver los resultados en un diccionario para su análisis
    return {
        "Utilidad": dict(Counter(seleccion_utilidad)),
        "Round-Robin": dict(Counter(seleccion_round_robin)),
        "Least Connections": dict(Counter(seleccion_least_connections))
    }

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
    
    for escenario in config["escenarios"]:
        print(f"\nEscenario: {escenario['nombre']}")
    
        resultados_metodos = tomar_decisiones_secuenciales(5, config["n_servidores"], *escenario["pesos"])

        print("\n📊 Resultados finales:")
    for metodo, resultado in resultados_metodos.items():
        print(f"🔹 Método {metodo}: {resultado}")

if __name__ == "__main__":
    main()
