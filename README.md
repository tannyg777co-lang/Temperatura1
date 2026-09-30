# Simulación de Flujo Continuo de Eventos — Arquitectura Kappa

**Proyecto de la materia de Big Data**  
*Universidad Politécnica de Querétaro (UPQ)*

**Integrantes:**
- Tanny Geraldine Correa Chávez
- Paola Regina Morales Jaimes
- Azul Salí Hernández Alarcón

---

##  Problema

Demostrar, con un modelo simplificado, cómo funciona la **arquitectura Kappa**: procesar la información principalmente como un flujo continuo de eventos, usando un log inmutable como fuente de verdad, en lugar de separar el procesamiento en una capa *batch* y una capa de tiempo real (como sucede en la arquitectura Lambda).

---

##  Datos

`sensores.csv` — Dataset de ejemplo con 90 lecturas de temperatura generadas para 3 sensores simulados (`sensor_A`, `sensor_B`, `sensor_C`).

| Columna | Descripción |
| :--- | :--- |
| `timestamp` | Fecha y hora de la lectura (formato ISO 8601) |
| `sensor` | Identificador único del sensor |
| `temperatura` | Lectura de temperatura en °C |

---


## Arquitectura y Solución

```text
sensores.csv ──> ( Productor ) ──> [ eventos.log ] ──> ( Consumidor ) ──> Estadísticas en vivo
                (Lee el CSV y       (Log append-only,   (Lee el log conforme
                 transmite fila      fuente de verdad)   llega y actualiza
                 por fila)                               conteo/prom/min/max)

----

====================================================================
INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN - ARQUITECTURA KAPPA
====================================================================

1. Clonar el repositorio
--------------------------------------------------------------------
Abre tu terminal o consola de comandos y ejecuta:

   git clone https://github.com/tannyg777co-lang/Temperatura1.git
   cd Temperatura1


2. Crear y activar un entorno virtual (Recomendado)
--------------------------------------------------------------------
Para aislar las dependencias del proyecto:

   En Windows (PowerShell / CMD):
      python -m venv .venv
      .venv\Scripts\activate

   En Linux / macOS:
      python3 -m venv .venv
      source .venv/bin/activate


3. Instalar las dependencias
--------------------------------------------------------------------
Instala los paquetes necesarios registrados en el archivo de requerimientos:

   pip install -r requirements.txt


4. Ejecutar la simulación
--------------------------------------------------------------------
Para iniciar el procesamiento de datos en tiempo real:

   python sensorestem.py

====================================================================
