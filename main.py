import random
import matplotlib.pyplot as plt
import networkx as nx


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
        if self.riesgo > 0:  # Amante del riesgo: aumenta utilidad si es incierto
            return utilidad_base + (self.riesgo * random.uniform(0, 0.1))
        elif self.riesgo < 0:  # Averso al riesgo: reduce utilidad si hay incertidumbre
            return utilidad_base - (abs(self.riesgo) * random.uniform(0, 0.1))
        else:
            return utilidad_base  # Neutral al riesgo

def seleccionar_mejor_servidor(servidores, w1, w2, w3, w4):
    """Selecciona el servidor con mayor utilidad esperada"""
    return max(servidores, key=lambda s: s.calcular_utilidad(w1, w2, w3, w4))

def generar_servidores(n):
    """Genera una lista de n servidores con valores aleatorios"""
    servidores = []
    for i in range(n):
        servidores.append(Server(
            id=i+1,
            carga=random.uniform(0, 1),
            latencia=random.uniform(0, 1),
            disponibilidad=random.choice([0, 1]),
            costo_migracion=random.uniform(0, 1),
            riesgo=random.uniform(-1, 1)  # Rango entre -1 (aversion) y 1 (amor por riesgo)
        ))
    return servidores

def simular_asignaciones(iteraciones, n_servidores, w1, w2, w3, w4):
    """Simula múltiples iteraciones de asignación de servidores y analiza resultados"""
    mejores_servidores = []
    
    for _ in range(iteraciones):
        servidores = generar_servidores(n_servidores)
        mejor = seleccionar_mejor_servidor(servidores, w1, w2, w3, w4)
        mejores_servidores.append(mejor.id)
    
    return mejores_servidores

def visualizar_resultados(mejores_servidores):
    """Grafica la frecuencia de selección de cada servidor"""
    plt.hist(mejores_servidores, bins=max(mejores_servidores), edgecolor='black', alpha=0.7)
    plt.xlabel("ID del Servidor")
    plt.ylabel("Frecuencia de Selección")
    plt.title("Distribución de la Selección de Servidores")
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
    # Parámetros de la simulación
    iteraciones = 1000   # Número de iteraciones de prueba
    n_servidores = 10    # Cantidad de servidores disponibles
    
    # Pesos de la función de utilidad (ajustables según importancia)
    w1, w2, w3, w4 = 0.4, 0.2, 0.3, 0.1

    # Ejecutar la simulación
    mejores_servidores = simular_asignaciones(iteraciones, n_servidores, w1, w2, w3, w4)
    
    # Visualizar resultados
    visualizar_resultados(mejores_servidores)

    # Generar diagrama de decisión
    generar_diagrama_decision()

    # Simular decisiones secuenciales (MDP)
    print("\n--- Simulación de Decisiones Secuenciales ---")
    tomar_decisiones_secuenciales(5, n_servidores, w1, w2, w3, w4)

if __name__ == "__main__":
    main()
