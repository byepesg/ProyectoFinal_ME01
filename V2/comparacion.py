import json
import matplotlib.pyplot as plt
from collections import Counter
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "input.json")

# === Implementación de Métodos Tradicionales ===
def round_robin(servidores, solicitudes):
    """Simula una asignación Round-Robin."""
    asignaciones = []
    n = len(servidores)
    for i in range(solicitudes):
        asignaciones.append(servidores[i % n].id)
    return asignaciones

import random

def least_connections(servidores, solicitudes):
    conexiones = {s.id: random.randint(1, 10) for s in servidores}  # 🔍 Agregar carga inicial aleatoria
    asignaciones = []
    
    for _ in range(solicitudes):
        servidor_menor_carga = min(conexiones, key=conexiones.get)
        asignaciones.append(servidor_menor_carga)
        conexiones[servidor_menor_carga] += 1  

    return asignaciones


# === Comparación de Algoritmos ===
def comparar_algoritmos(config, servidores, seleccionar_mejor_servidor):
    """Compara la selección de servidores usando función de utilidad, Round-Robin y Least Connections"""
    iteraciones = config["iteraciones"]

    resultados = {"Utilidad": {}, "Round-Robin": {}, "Least Connections": {}}

    # Simulación de utilidad
    for escenario in config["escenarios"]:
        w1, w2, w3, w4 = escenario["pesos"]
        mejores_servidores = [seleccionar_mejor_servidor(servidores, w1, w2, w3, w4).id for _ in range(iteraciones)]
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
    
    print("Debug - Estructura de resultados:", json.dumps(resultados, indent=4))  # 🔍 Inspección de datos
    
    for metodo, datos in resultados.items():
        plt.figure(figsize=(8, 5))

        for escenario, conteo in datos.items():
            if not isinstance(conteo, dict):  # 🔍 Evitar errores si conteo no es diccionario
                print(f"⚠️ Error: conteo en '{escenario}' no es un diccionario, sino {type(conteo)} -> {conteo}")
                continue  # Salta este escenario para evitar el error

            plt.bar(conteo.keys(), conteo.values(), alpha=0.7, label=escenario)

        plt.xlabel("ID del Servidor")
        plt.ylabel("Frecuencia de Selección")
        plt.title(f"Comparación de Selección de Servidores - {metodo}")
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()


# === Cálculo de Métricas de Desempeño ===
def calcular_metricas(resultados):
    """Calcula métricas como tiempo de respuesta promedio y balanceo de carga"""
    metricas = {}
    for metodo, escenarios in resultados.items():
        metricas[metodo] = {}
        for escenario, conteo in escenarios.items():
            if not isinstance(conteo, dict):  # 🔍 Evitar errores si conteo no es diccionario
                print(f"⚠️ Error: conteo en '{escenario}' no es un diccionario, sino {type(conteo)} -> {conteo}")
                continue
            
            total_selecciones = sum(conteo.values()) if len(conteo) > 0 else 0
            promedio = total_selecciones / len(conteo) if len(conteo) > 0 else 0
            dispersion = max(conteo.values()) - min(conteo.values()) if len(conteo) > 1 else 0
            metricas[metodo][escenario] = {
                "Total Selecciones": total_selecciones,
                "Promedio por Servidor": promedio,
                "Diferencia Máx-Mín": dispersion
            }
    return metricas
def graficar_least_connections(resultados):
    """Genera un gráfico de barras para visualizar la distribución de carga en Least Connections"""
    datos = resultados["Least Connections"]["General"]  # Obtener los datos
    servidores = list(datos.keys())
    cargas = list(datos.values())

    plt.figure(figsize=(8,5))
    plt.bar(servidores, cargas, color='blue', alpha=0.7)
    plt.xlabel("ID del Servidor")
    plt.ylabel("Solicitudes Asignadas")
    plt.title("Distribución de Carga - Least Connections")
    plt.xticks(rotation=45)
    plt.show()



# === Flujo Principal (Ejecutar esto aparte o en un archivo separado) ===
if __name__ == "__main__":
    # Leer configuración de input.json
    with open(input_path, "r") as file:
        config = json.load(file)  # ✅ Convertimos la cadena JSON en un diccionario de Python

    
    # Importar la función original de mainMejorado.py
    from mainMejorado import generar_servidores, seleccionar_mejor_servidor

    # Generar servidores
    servidores = generar_servidores(config["n_servidores"])

    # Comparar algoritmos
    resultados = comparar_algoritmos(config, servidores, seleccionar_mejor_servidor)

    # Guardar resultados en output.json
    with open("output_comparacion.json", "w") as file:
        json.dump(resultados, file, indent=4)
    # Llamar la función después de calcular resultados
    graficar_least_connections(resultados)
    # Graficar comparación
    visualizar_comparacion(resultados)

    # Calcular métricas y guardarlas en metricas.json
    metricas = calcular_metricas(resultados)
    with open("metricas.json", "w") as file:
        json.dump(metricas, file, indent=4)

    print("Comparación completada. Resultados guardados en 'output_comparacion.json' y métricas en 'metricas.json'.")
