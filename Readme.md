# Proyecto ME01

- Brayan Sebastián Yepes García
- Diana Marcela Bello López

python3 -m venv myenv

source myenv/bin/activate


pip install numpy pandas matplotlib


pip freeze > requirements.txt


pip install -r requirements.txt


# Proyecto de Selección y Comparación de Servidores

Este proyecto en Python permite **simular**, **comparar** y **visualizar** diferentes estrategias para la asignación de solicitudes a servidores. Se utilizan criterios de utilidad (considerando carga, latencia, disponibilidad, costo de energía, tolerancia a fallos, etc.), así como algoritmos clásicos de balanceo de carga (Round-Robin y Least Connections).  

## Características Principales
1. **Generación Aleatoria de Servidores**: Crea servidores con valores aleatorios para parámetros como carga, latencia, disponibilidad, costo de migración, riesgo, costo de energía y tolerancia a fallos.
2. **Función de Utilidad**: Calcula una utilidad que combina múltiples criterios con pesos configurables.
3. **Ajuste Dinámico de Pesos**: Modifica los pesos de la función de utilidad en función de la carga y latencia promedio.
4. **Comparación de Algoritmos**:
   - Selección según la función de utilidad
   - Round-Robin
   - Least Connections
5. **Simulación de Escenarios**: Ejecuta múltiples iteraciones y muestra la frecuencia de selección de cada servidor.
6. **Visualización de Resultados**: Genera gráficas de barras y un diagrama de decisión.
7. **Resultados en Archivos**:
   - `output_comparacion.json`: Resultados de la comparación entre métodos de asignación.  
   - Gráficas `.png`: Se generan archivos PNG con las visualizaciones.  

---

## Requisitos
- Python 3.x
- Librerías:
  - `matplotlib`
  - `networkx`
  - `json` (Biblioteca estándar)
  - `random` (Biblioteca estándar)
  - `collections` (Biblioteca estándar)
  - `os`, `sys`, `io` (Biblioteca estándar)

Puedes instalarlas con:
```bash
pip install matplotlib networkx
```
(El resto de librerías vienen incluidas en la biblioteca estándar de Python.)

---

## Estructura de Archivos
- **`mainComparacion.py`**: Contiene todo el código fuente principal.
- **`input.json`**: Archivo de entrada para la configuración de escenarios.  
- **`output_comparacion.json`**: Archivo de salida que se genera con los resultados de la comparación entre algoritmos.
- **`grafico_{escenario}.png`**: Gráficas de frecuencia de selección de servidores para cada escenario.
- **`diagrama_decision.png`**: Diagrama de decisión en formato PNG.

---

## Formato de `input.json`
Un ejemplo de archivo de configuración podría verse así:
```json
{
  "n_servidores": 5,
  "iteraciones": 50,
  "escenarios": [
    {
      "nombre": "Escenario_1",
      "pesos": [0.3, 0.2, 0.3, 0.2]
    },
    {
      "nombre": "Escenario_2",
      "pesos": [0.1, 0.4, 0.4, 0.1]
    }
  ]
}
```

---

## Ejecución
1. Clona o descarga el repositorio en tu máquina local.
2. Asegúrate de tener instalado Python 3.
3. Instala las dependencias (si no las tuvieras):
   ```bash
   pip install matplotlib networkx
   ```
4. Verifica que exista un archivo `input.json` con la configuración deseada.
5. Ejecuta el script:
   ```bash
   python script.py
   ```
6. Se generarán:
   - **Archivos `.png`** con las gráficas resultantes (`grafico_{Escenario}.png` y `diagrama_decision.png`).
   - El archivo **`output_comparacion.json`** con los resultados de la comparación entre algoritmos.

---

## Descripción General del Código

### Clase `Server`
Representa un servidor con atributos como:
- `id`, `carga`, `latencia`, `disponibilidad`, `costo_migracion`, `riesgo`, `costo_energia`, `tolerancia_fallos`.

La función `calcular_utilidad(self, *pesos)` combina estos atributos con distintos **pesos** para producir una **utilidad**.

### Funciones Principales

1. **`ajustar_pesos_dinamicamente(servidores)`**  
   Ajusta los pesos de la función de utilidad con base en la carga y la latencia promedio.

2. **`seleccionar_mejor_servidor(servidores)`**  
   Selecciona el servidor con **mayor** utilidad usando pesos dinámicos.

3. **`simular_escenarios(config)`**  
   Corre múltiples escenarios según la configuración en `input.json`, y registra cuál servidor es elegido con más frecuencia.

4. **Algoritmos de Asignación**:
   - **`round_robin(servidores, solicitudes)`**: Asigna solicitudes de forma cíclica.  
   - **`least_connections(servidores, solicitudes)`**: Asigna solicitudes al servidor con menos conexiones.

5. **`comparar_algoritmos(config, servidores)`**  
   Compara **Utilidad**, **Round-Robin** y **Least Connections** mediante múltiples iteraciones.

6. **`visualizar_comparacion(resultados)`**  
   Muestra en pantalla (con `plt.show()`) las gráficas comparativas entre estos tres métodos.

---

## Agradecimientos