# Proyecto ME01

## Descripción
Proyecto ME01 es una aplicación desarrollada en Python que utiliza `numpy`, `pandas` y `matplotlib` para el análisis y visualización de datos. Este documento proporciona instrucciones detalladas para configurar el entorno y ejecutar el proyecto.

## Requisitos previos
Antes de comenzar, asegúrate de tener instalado lo siguiente:
- Python 3.x (Se recomienda la última versión estable)
- Git (opcional, para clonar el repositorio)

Para verificar si tienes Python instalado, ejecuta:
```sh
python3 --version
```

Si Python no está instalado, puedes descargarlo desde [python.org](https://www.python.org/downloads/).

## Instalación
Sigue los siguientes pasos para configurar el entorno de desarrollo:

### 1. Clonar el repositorio (opcional)
Si estás trabajando desde un repositorio de GitHub, clónalo con:
```sh
git clone https://github.com/tuusuario/ProyectoME01.git
cd ProyectoME01
```

### 2. Crear y activar un entorno virtual
Para aislar las dependencias del proyecto, crea un entorno virtual:
```sh
python3 -m venv myenv
source myenv/bin/activate  # En Linux/macOS
myenv\Scripts\activate    # En Windows
```

### 3. Instalar dependencias
Ejecuta el siguiente comando para instalar las dependencias necesarias:
```sh
pip install -r requirements.txt
```

Si deseas instalar los paquetes manualmente, puedes hacerlo con:
```sh
pip install numpy pandas matplotlib
```

### 4. Verificar la instalación
Para asegurarte de que todo esté funcionando correctamente, prueba ejecutando el siguiente script en Python:
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Instalación exitosa")
```
Si ves el mensaje `Instalación exitosa`, la configuración está completa.

## Uso del Proyecto
Para ejecutar el código principal del proyecto, usa:
```sh
python main.py
```

Si el proyecto está estructurado en módulos, asegúrate de ejecutarlo desde la ruta correcta.

## Notas adicionales
- Si agregas nuevas dependencias, recuerda actualizarlas en `requirements.txt` con:
  ```sh
  pip freeze > requirements.txt
  ```
- Para salir del entorno virtual, usa:
  ```sh
deactivate
  ```

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

