import json
import random
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import os
import io
import sys
import numpy as np
import random 
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join("F:\\ProyectoEstoc", "input.json")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
json_path = os.path.join("F:\\ProyectoEstoc", "output_comparacion.json")

# Cargar datos desde el JSON
def cargar_datos(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

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

    def generar_escenarios_aleatorios(n):
        """Genera escenarios con pesos distribuidos de manera equitativa"""
        nombres = ["Balanceado", "Baja Latencia", "Alta Disponibilidad", "Costo Energético Bajo", "Alta Tolerancia a Fallos"]
        escenarios = []
        
        for nombre in nombres[:n]:
            num_pesos = 6  # Asegurar que siempre haya 6 pesos
            pesos = np.random.dirichlet(np.ones(num_pesos), size=1)[0].tolist()  # Suman 1.0
            escenarios.append({"nombre": nombre, "pesos": pesos})
        
        return escenarios


    def calcular_utilidad(self, *pesos):
        """Calcula la función de utilidad con mejor normalización y balance"""
        if len(pesos) < 4:
            raise ValueError("Se requieren al menos 4 pesos para calcular la utilidad.")

        # Asignar pesos
        w1, w2, w3, w4 = pesos[:4]
        w5 = pesos[4] if len(pesos) > 4 else 0.15  # Reducimos el impacto de energía
        w6 = pesos[5] if len(pesos) > 5 else 0.15  # Reducimos el impacto de fallos

        # Aplicamos normalización con valores más justos
        carga_norm = (self.carga - 0.3) / 0.4  
        latencia_norm = (self.latencia - 0.3) / 0.4
        disponibilidad_norm = (self.disponibilidad - 0.7) / 0.3
        costo_migracion_norm = (self.costo_migracion - 0.3) / 0.4
        costo_energia_norm = (self.costo_energia - 0.3) / 0.4
        tolerancia_fallos_norm = (self.tolerancia_fallos - 0.5) / 0.4  

        # Nueva forma de calcular utilidad con menos peso en latencia y disponibilidad
        utilidad_base = (
            w1 * (1 - carga_norm) +
            w2 * (1 - costo_migracion_norm) +
            w3 * (0.5 - latencia_norm) +  # Hacemos que la latencia no influya tanto
            w4 * (0.5 + disponibilidad_norm) +  # Reducimos el impacto de disponibilidad
            w5 * (0.5 - costo_energia_norm) +
            w6 * (0.5 + tolerancia_fallos_norm)
        )

        # Penalización por riesgo ajustada para evitar sesgos
        if self.riesgo > 0:
            utilidad_base *= (1 - self.riesgo * 0.05)  # Menos impacto negativo
        elif self.riesgo < 0:
            utilidad_base *= (1 + abs(self.riesgo) * 0.05)

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


def generar_servidores(n):
    """Genera servidores con atributos más balanceados"""
    servidores = []
    valores = np.linspace(0.3, 0.7, n)  # Distribuye valores equitativamente

    for i in range(n):
        random.shuffle(valores)  # Mezcla valores para evitar patrones repetitivos
        servidores.append(Server(
            id=i+1,
            carga=valores[i],
            latencia=valores[-(i+1)],
            disponibilidad=random.uniform(0.7, 1.0),
            costo_migracion=valores[i],
            riesgo=random.uniform(-0.2, 0.2),  # Reducimos la variación de riesgo
            costo_energia=valores[-(i+1)],
            tolerancia_fallos=random.uniform(0.5, 0.9)
        ))

    return servidores

def analizar_utilidad_servidores(servidores, pesos):
    """Imprime la utilidad calculada de cada servidor en una iteración"""
    print("\n📊 Análisis de utilidad por servidor:")
    for s in servidores:
        utilidad = s.calcular_utilidad(*pesos)
        print(f"Servidor {s.id} -> Utilidad: {utilidad:.4f}")
servidores = generar_servidores(10)
pesos = ajustar_pesos_dinamicamente(servidores)

print(f"\n🔍 Pesos aplicados: {pesos}")



def seleccionar_mejor_servidor(servidores):
    """Selecciona el mejor servidor con más aleatoriedad entre los Top 5"""
    pesos_dinamicos = ajustar_pesos_dinamicamente(servidores)
    utilidades = [(s.id, s.calcular_utilidad(*pesos_dinamicos)) for s in servidores]

    # Ordenar servidores por utilidad de mayor a menor
    utilidades.sort(key=lambda x: x[1], reverse=True)

    # Elegir aleatoriamente entre los 5 mejores (más variabilidad)
    top_5 = utilidades[:5]
    mejor_servidor = random.choice(top_5)

    print(f"🔹 Servidores Top 5: {top_5}")  # Para ver si el sesgo desaparece

    return next(s for s in servidores if s.id == mejor_servidor[0])


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
        colores = plt.cm.tab10(np.linspace(0, 1, len(datos)))  # Genera una lista de colores distintos

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
# Función para graficar los datos extraídos del JSON
def graficar_resultados(resultados):
    # Extraer los escenarios de utilidad
    escenarios = resultados.get("Utilidad", {}).keys()
    
    # Gráfico de barras agrupadas con todos los métodos
    plt.figure(figsize=(10, 6))
    servidores = set()
    utilidad_escenarios = {}
    
    for escenario in escenarios:
        utilidad_data = resultados["Utilidad"].get(escenario, {})
        utilidad_escenarios[escenario] = utilidad_data
        servidores.update(map(int, utilidad_data.keys()))
    
    round_robin_data = resultados["Round-Robin"].get("General", {})
    least_connections_data = resultados["Least Connections"].get("General", {})
    servidores.update(map(int, round_robin_data.keys()))
    servidores.update(map(int, least_connections_data.keys()))
    servidores = sorted(servidores)
    
    x = np.arange(len(servidores))
    width = 0.25  # Ancho de las barras
    
    # Construcción de datos para graficar
    for i, escenario in enumerate(escenarios):
        utilidad_valores = [utilidad_escenarios[escenario].get(str(s), 0) for s in servidores]
        plt.bar(x - width + (i * width / len(escenarios)), utilidad_valores, width / len(escenarios), label=f"{escenario}", alpha=0.7)
    
    round_robin_valores = [round_robin_data.get(str(s), 0) for s in servidores]
    least_connections_valores = [least_connections_data.get(str(s), 0) for s in servidores]
    
    plt.bar(x, round_robin_valores, width, label="Round-Robin", color='red', alpha=0.7)
    plt.bar(x + width, least_connections_valores, width, label="Least Connections", color='green', alpha=0.7)
    
    # Configuración del gráfico
    plt.xlabel("ID del Servidor")
    plt.ylabel("Frecuencia de Selección")
    plt.title("Comparación de Algoritmos - General")
    plt.xticks(x, servidores)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Mostrar gráfico agrupado
    plt.show()
    
    # Gráficos individuales por escenario
    for escenario in escenarios:
        plt.figure(figsize=(10, 6))
        
        utilidad_data = resultados["Utilidad"].get(escenario, {})
        utilidad_valores = [utilidad_data.get(str(s), 0) for s in servidores]
        
        plt.bar(x - width, utilidad_valores, width, label="Utilidad", color='blue', alpha=0.7)
        plt.bar(x, round_robin_valores, width, label="Round-Robin", color='red', alpha=0.7)
        plt.bar(x + width, least_connections_valores, width, label="Least Connections", color='green', alpha=0.7)
        
        # Configuración del gráfico
        plt.xlabel("ID del Servidor")
        plt.ylabel("Frecuencia de Selección")
        plt.title(f"Comparación de Algoritmos - {escenario}")
        plt.xticks(x, servidores)
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Mostrar gráfico
        plt.show()
def graficar_seleccion_servidores(resultados):
    """Grafica la cantidad de veces que cada servidor fue elegido"""
    conteo = Counter(resultados)

    plt.figure(figsize=(8, 5))
    plt.bar(conteo.keys(), conteo.values(), color='blue', alpha=0.7)
    plt.xlabel("ID del Servidor")
    plt.ylabel("Frecuencia de Selección")
    plt.title("Distribución Final de Selección de Servidores")
    plt.xticks(list(conteo.keys()))
    plt.show()

servidores = generar_servidores(10)
selecciones = [seleccionar_mejor_servidor(servidores).id for _ in range(100)]
graficar_seleccion_servidores(selecciones)

def guardar_resultados(resultados, json_path):
    """Guarda los resultados en un archivo JSON"""
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(resultados, file, indent=4, ensure_ascii=False)
    print(f"✅ Archivo guardado en: {json_path}")

if __name__ == "__main__":
    if os.path.exists(json_path):
        datos = cargar_datos(json_path)
        graficar_resultados(datos)
    else:
        print(f"Error: No se encontró el archivo {json_path}")
