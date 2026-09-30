"""
Simulación de flujo continuo de eventos (estilo Kappa).

- Productor: lee el dataset sensores.csv fila por fila y va agregando
  cada lectura al log de eventos (eventos.log, append-only).
- Consumidor: lee el log conforme llega y actualiza estadísticas
  continuamente con pandas y las renderiza con rich.

Dataset: sensores.csv (90 lecturas de temperatura de 3 sensores).

Ejecutar: python kappa_demo.py
"""
import json
import threading
import time
import pandas as pd
from rich.console import Console
from rich.table import Table

DATASET = "sensores.csv"
LOG_FILE = "eventos.log"
INTERVALO = 0.3  # segundos entre eventos

console = Console()


def productor(detener):
    """Lee el dataset y transmite cada fila como un evento del stream."""
    df = pd.read_csv(DATASET)
    
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        for _, fila in df.iterrows():
            if detener.is_set():
                break
            evento = {
                "timestamp": str(fila["timestamp"]),
                "sensor": str(fila["sensor"]),
                "temperatura": float(fila["temperatura"]),
            }
            log.write(json.dumps(evento) + "\n")
            log.flush()
            time.sleep(INTERVALO)
            
    detener.set()  # avisa al consumidor que no llegarán más eventos


def consumidor(detener):
    """Lee el log en tiempo real y muestra métricas actualizadas con pandas y rich."""
    eventos = []
    
    with open(LOG_FILE, "r", encoding="utf-8") as log:
        while True:
            linea = log.readline()
            if not linea:
                if detener.is_set():
                    break
                time.sleep(0.1)
                continue
            
            e = json.loads(linea)
            eventos.append(e)
            
            # Procesar datos acumulados usando pandas
            df_stream = pd.DataFrame(eventos)
            stats = df_stream.groupby("sensor")["temperatura"].agg(
                n="count",
                prom="mean",
                min="min",
                max="max"
            ).reset_index()

            # Construir tabla visual con rich
            table = Table(title=f"Stream activo | Última lectura: [{e['timestamp']}] {e['sensor']} = {e['temperatura']}°C")
            table.add_column("Sensor", style="cyan", no_wrap=True)
            table.add_column("Lecturas (n)", style="magenta")
            table.add_column("Promedio (°C)", style="green")
            table.add_column("Mínimo (°C)", style="blue")
            table.add_column("Máximo (°C)", style="red")

            for _, row in stats.iterrows():
                table.add_row(
                    str(row["sensor"]),
                    str(int(row["n"])),
                    f"{row['prom']:.2f}",
                    f"{row['min']:.2f}",
                    f"{row['max']:.2f}"
                )

            console.clear()
            console.print(table)


if __name__ == "__main__":
    open(LOG_FILE, "w").close()  # reinicia el log
    detener = threading.Event()
    
    hilos = [
        threading.Thread(target=productor, args=(detener,)),
        threading.Thread(target=consumidor, args=(detener,)),
    ]
    
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
        
    console.print("\n[bold green]Fin de la simulación.[/bold green]")