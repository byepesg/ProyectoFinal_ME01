import json
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import os
import io
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "input.json")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Server:
    """Clase que representa un servidor con sus características clave"""
    
    def __init__(self, id, carga, latencia, disponibilidad, costo_migracion, riesgo, costo_energia, tolerancia_fallos):
        self.id = id
        self.carga = carga  
        self.latencia = latencia  
        self.disponibilidad = disponibilidad  
        self.costo_migracion = costo_migracion  
        self.riesgo = riesgo  
        self.costo_energia = costo_energia  
        self.tolerancia_fallos = tolerancia_fallos  

    def calcular_utilidad(self, *pesos):
        """Calcula la función de utilidad considerando costo energético y tolerancia a fallos"""
        if len(pesos) < 4:
            raise ValueError("Se requieren al menos 4 pesos para calcular la utilidad.")
        
        # Asignar pesos a las variables correspondientes
        w1, w2, w3, w4 = pesos[:4]
        w5 = pesos[4] if len(pesos) > 4 else 0.1  # Valor predeterminado para w5
        w6 = pesos[5] if len(pesos) > 5 else 0.1  # Valor predeterminado para w6

        utilidad_base = (w1 * (1 - self.carga) +
                        w2 * (1 - self.costo_migracion) +
                        w3 * (1 - self.latencia) +
                        w4 * self.disponibilidad +
                        w5 * (1 - self.costo_energia) +
                        w6 * self.tolerancia_fallos)

        if self.riesgo > 0:  
            return utilidad_base + (self.riesgo * random.uniform(0, 0.1))
        elif self.riesgo < 0:  
            return utilidad_base - (abs(self.riesgo) * random.uniform(0, 0.1))
        else:
            return utilidad_base
def ajustar_pesos_dinamicamente(servidores):
    """Ajusta los pesos según la carga promedio y latencia"""
    carga_promedio = sum(s.carga for s in servidores) / len(servidores)
    latencia_promedio = sum(s.latencia for s in servidores) / len(servidores)

    # Pesos base
    w_carga = 0.3
    w_migracion = 0.2
    w_latencia = 0.3
    w_disponibilidad = 0.2

    if carga_promedio > 0.7:
        w_carga = 0.1  
        w_latencia = 0.5  
        w_disponibilidad = 0.4  

    if latencia_promedio > 0.5:
        w_latencia = 0.5  
        w_migracion = 0.1  

    suma_pesos = w_carga + w_migracion + w_latencia + w_disponibilidad
    return [w_carga / suma_pesos, w_migracion / suma_pesos, w_latencia / suma_pesos, w_disponibilidad / suma_pesos]

def seleccionar_mejor_servidor(servidores):
    """Selecciona el servidor con mayor utilidad esperada usando pesos dinámicos"""
    pesos_dinamicos = ajustar_pesos_dinamicamente(servidores)
    return max(servidores, key=lambda s: s.calcular_utilidad(*pesos_dinamicos))

def generar_servidores(n, distribucion="beta"):
    """Genera una lista de servidores con valores balanceados"""
    return [
        Server(
            id=i+1,
            carga=random.uniform(0.2, 0.8),
            latencia=random.uniform(0.2, 0.8),
            disponibilidad=random.uniform(0.7, 1.0),
            costo_migracion=random.uniform(0.2, 0.8),
            riesgo=random.uniform(-0.5, 0.5),
            costo_energia=random.uniform(0.2, 0.8),
            tolerancia_fallos=random.uniform(0.5, 1.0)
        )
        for i in range(n)
    ]

def simular_escenarios(config):
    """Ejecuta simulaciones para múltiples escenarios y guarda resultados"""
    resultados = {}

    for escenario in config["escenarios"]:
        iteraciones = config["iteraciones"]
        n_servidores = config["n_servidores"]
        
        # Verifica que haya al menos 4 pesos
        if len(escenario["pesos"]) < 4:
            raise ValueError(f"El escenario '{escenario['nombre']}' debe tener al menos 4 pesos.")
        
        # Usa todos los pesos proporcionados
        pesos = escenario["pesos"]

        mejores_servidores = []
        for _ in range(iteraciones):
            servidores = generar_servidores(n_servidores)
            mejor = max(servidores, key=lambda s: s.calcular_utilidad(*pesos))
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
        
        plt.savefig(f"grafico_{escenario}.png", bbox_inches="tight")
        print(f"📊 Imagen guardada: grafico_{escenario}.png")
        plt.close()

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
    
    plt.savefig("diagrama_decision.png", bbox_inches="tight")
    print("📊 Imagen guardada: diagrama_decision.png")
    plt.close()

def round_robin(servidores, solicitudes):
    """Simula una asignación Round-Robin."""
    asignaciones = []
    n = len(servidores)
    for i in range(solicitudes):
        asignaciones.append(servidores[i % n].id)
    return asignaciones

def least_connections(servidores, solicitudes):
    """Simula asignación de solicitudes al servidor con menos carga"""
    conexiones = {s.id: random.randint(1, 10) for s in servidores}  
    asignaciones = []
    
    for _ in range(solicitudes):
        servidor_menor_carga = min(conexiones, key=conexiones.get)
        asignaciones.append(servidor_menor_carga)
        conexiones[servidor_menor_carga] += 1  

    return asignaciones

def comparar_algoritmos(config, servidores):
    """Compara la selección de servidores usando función de utilidad, Round-Robin y Least Connections"""
    iteraciones = config["iteraciones"]
    resultados = {"Utilidad": {}, "Round-Robin": {}, "Least Connections": {}}

    # Simulación de utilidad
    for escenario in config["escenarios"]:
        mejores_servidores = [seleccionar_mejor_servidor(servidores).id for _ in range(iteraciones)]
        resultados["Utilidad"][escenario["nombre"]] = dict(Counter(mejores_servidores))

    # Simulación Round-Robin
    asignaciones_rr = round_robin(servidores, iteraciones)
    resultados["Round-Robin"]["General"] = dict(Counter(asignaciones_rr))

    # Simulación Least Connections
    asignaciones_lc = least_connections(servidores, iteraciones)
    resultados["Least Connections"]["General"] = dict(Counter(asignaciones_lc))

    return resultados

def visualizar_comparacion(resultados):
    """Grafica la comparación entre métodos de selección de servidores"""
    print("Debug - Estructura de resultados:", json.dumps(resultados, indent=4))
    
    for metodo, datos in resultados.items():
        plt.figure(figsize=(8, 5))

        for escenario, conteo in datos.items():
            if not isinstance(conteo, dict):  
                print(f"⚠️ Error en '{escenario}': {type(conteo)} -> {conteo}")
                continue  

            plt.bar(conteo.keys(), conteo.values(), alpha=0.7, label=escenario)

        plt.xlabel("ID del Servidor")
        plt.ylabel("Frecuencia de Selección")
        plt.title(f"Comparación - {metodo}")
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()

def main():
    """Ejecución del programa principal"""
    with open(input_path, "r") as file:
        config = json.load(file)
    
    # Generar servidores
    servidores = generar_servidores(config["n_servidores"])

    # Comparar algoritmos
    resultados = comparar_algoritmos(config, servidores)

    # Guardar resultados
    with open("output_comparacion.json", "w") as file:
        json.dump(resultados, file, indent=4)

    # Visualizar comparación
    visualizar_comparacion(resultados)

    # Simular escenarios y visualizar resultados
    resultados_simulacion = simular_escenarios(config)
    visualizar_resultados(resultados_simulacion)

    # Generar diagrama de decisión
    generar_diagrama_decision()

    print("Comparación completada. Resultados guardados en 'output_comparacion.json'.")

if __name__ == "__main__":
    main()