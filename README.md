# Simulación de flujo continuo de eventos — Arquitectura Kappa

Proyecto de la materia de Big Data — Universidad Politécnica de Querétaro (UPQ).

**Integrantes:** Tanny Geraldine Correa Chávez, Paola Regina Morales Jaimes, Azul Dalí Hernández Alarcón.

## Problema

Demostrar, con un modelo simplificado, cómo funciona la arquitectura Kappa: procesar
la información principalmente como un flujo continuo de eventos, usando un log
inmutable como fuente de verdad, en lugar de separar el procesamiento en una capa
batch y una capa de tiempo real (como hace la arquitectura Lambda).

## Datos

`sensores.csv` — dataset de ejemplo con 90 lecturas de temperatura generadas para
3 sensores simulados (`sensor_A`, `sensor_B`, `sensor_C`). Columnas:

| columna      | descripción                        |
|--------------|-------------------------------------|
| timestamp    | fecha y hora de la lectura (ISO 8601) |
| sensor       | identificador del sensor            |
| temperatura  | lectura en °C                       |

## Arquitectura / solución

```
sensores.csv → Productor → eventos.log → Consumidor → Estadísticas en vivo
                (lee el CSV               (log append-only,   (lee el log conforme
                 y transmite               fuente de verdad)    llega y actualiza
                 fila por fila)                                 conteo/prom/min/max)
```

- **Productor**: lee `sensores.csv` fila por fila y va agregando cada lectura a
  `eventos.log`, simulando que los datos llegan en tiempo real (una lectura cada
  0.3 s).
- **Log de eventos** (`eventos.log`): archivo *append-only* donde cada línea es un
  evento en formato JSON. Es la fuente de verdad del sistema, igual que en Kappa.
- **Consumidor**: lee el log conforme se van escribiendo eventos nuevos, acumula los
  eventos en un DataFrame de `pandas` y recalcula con `groupby` las estadísticas por
  sensor (número de lecturas, promedio, mínimo y máximo), mostrándolas en una tabla
  en vivo en la terminal con `rich`.

Productor y consumidor corren en paralelo (dos hilos), comunicándose únicamente a
través del log, tal como en Kappa un componente nuevo podría reprocesar el stream
completo volviendo a leer el log desde el inicio.

## Instalación

Se necesita Python 3.9+ y las dependencias listadas en `requirements.txt` (`pandas`
para las estadísticas y `rich` para la tabla en la terminal).

```bash
git clone https://github.com/tannyg777co-lang/Temperatura1.git
cd <Temperatura1>
pip install -r requirements.txt
```

## Ejecución

```bash
python sensorestem.py
```

El script:
1. Reinicia `eventos.log`.
2. Levanta el productor y el consumidor en hilos paralelos.
3. Imprime cada evento conforme llega, con las estadísticas actualizadas.
4. Al terminar de leer las 90 filas, imprime un resumen final por sensor.

## Resultados / interpretación

Con las 90 lecturas del dataset, el consumidor termina reportando, por cada
sensor, cuántas lecturas procesó y su promedio, mínimo y máximo — todo calculado
de forma incremental, evento por evento, sin necesidad de tener todos los datos
cargados de antemano. Esto ilustra la idea central de Kappa: un solo camino de
procesamiento (streaming) es suficiente tanto para ver resultados en tiempo real
como para recalcular todo el histórico, ya que basta con volver a leer el log.

## Estructura del repositorio

```
.
├── sensorestem.py      # productor + consumidor
├── sensores.csv        # dataset de ejemplo
├── requirements.txt
└── README.md
```
