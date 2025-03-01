import json
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

class Server:
    """Clase que representa un servidor con sus características clave"""

    def __init__(self, id, carga, latencia, disponibilidad, costo_migracion, riesgo):
        self.id = id
        self.carga = carga  # Carga actual del servidor (0 a 1)
        self.latencia = latencia  # Latencia en ms (0 a 500 normalizado)
        self.disponibilidad = disponibilidad  # Disponibilidad binaria (0 o 1)
        self.costo_migracion = costo_migracion  # Costo de mover una instancia a este servidor (0 a 1)
        self.riesgo = riesgo  # Nivel de riesgo (-1 a 1)

    def calcular_utilidad(self, w1, w2, w3, w4, w5):
        """Calcula la función de utilidad balanceada"""
        utilidad_base = (w1 * (1 - self.carga) +
                         w2 * (1 - self.costo_migracion) +
                         w3 * (1 - self.latencia) +
                         w4 * self.disponibilidad +
                         w5 * (1 - abs(self.riesgo)))  # Prefiere servidores con menor riesgo

        return max(0, min(1, utilidad_base))  # Asegurar valores entre 0 y 1


def seleccionar_mejor_servidor(servidores, w1, w2, w3, w4, w5):
    """Selecciona el servidor con mayor utilidad esperada"""
    return max(servidores, key=lambda s: s.calcular_utilidad(w1, w2, w3, w4, w5))


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
    else:
        raise ValueError(f"Distribución '{distribucion}' no reconocida.")


def generar_servidores(n, distribucion="normal"):
    """Genera una lista de n servidores con valores iniciales equilibrados"""
    return [
        Server(
            id=i + 1,
            carga=generar_valor_con_distribucion(distribucion, mu=0.5, sigma=0.2),
            latencia=generar_valor_con_distribucion(distribucion, mu=0.3, sigma=0.1),
            disponibilidad=random.choice([0, 1]),
            costo_migracion=generar_valor_con_distribucion(distribucion, mu=0.4, sigma=0.15),
            riesgo=random.uniform(-0.5, 0.5)
        )
        for i in range(n)
    ]


def simular_escenarios(config):
    """Ejecuta simulaciones para múltiples escenarios y guarda la evolución de carga"""
    resultados = defaultdict(list)

    for escenario in config["escenarios"]:
        iteraciones = config["iteraciones"]
        n_servidores = config["n_servidores"]
        pesos = escenario["pesos"]

        # Si hay más de 5 pesos, tomar solo los primeros 5
        if len(pesos) > 5:
            pesos = pesos[:5]
        # Si hay menos de 5 pesos, rellenar con ceros
        elif len(pesos) < 5:
            pesos += [0] * (5 - len(pesos))

        # Asignar los valores corregidos
        w1, w2, w3, w4, w5 = pesos

        servidores = generar_servidores(n_servidores)

        for _ in range(iteraciones):
            mejor = seleccionar_mejor_servidor(servidores, w1, w2, w3, w4, w5)
            resultados[mejor.id].append(mejor.carga)

            # Simulación de ajuste de carga
            for server in servidores:
                server.carga = min(1, max(0, server.carga + random.uniform(-0.05, 0.05)))

    return resultados


def visualizar_carga_servidores(resultados):
    """Grafica la evolución de la carga de los servidores"""
    plt.figure(figsize=(10, 6))

    for id_servidor, cargas in resultados.items():
        plt.plot(range(len(cargas)), cargas, label=f"Servidor {id_servidor}", alpha=0.7)

    plt.xlabel("Iteraciones")
    plt.ylabel("Carga del Servidor")
    plt.title("Evolución de Carga en los Servidores")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()


def generar_diagrama_decision():
    """Genera un diagrama de decisión visual"""
    G = nx.DiGraph()

    G.add_node("Inicio")
    for i in range(1, 4):
        G.add_node(f"Servidor {i}")
        G.add_edge("Inicio", f"Servidor {i}", label=f"Opción {i}")

    G.add_node("Decisión final")
    for i in range(1, 4):
        G.add_edge(f"Servidor {i}", "Decisión final", label="Evalúa Utilidad")

    plt.figure(figsize=(8, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, edge_color='gray')
    edge_labels = {(i, j): G.edges[i, j]['label'] for i, j in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Diagrama de Decisión para Selección de Servidores")
    plt.show()


def main():
    with open("input.json", "r") as file:
        config = json.load(file)

    resultados = simular_escenarios(config)

    with open("output.json", "w") as file:
        json.dump(resultados, file, indent=4)

    visualizar_carga_servidores(resultados)
    generar_diagrama_decision()


if __name__ == "__main__":
    main()
