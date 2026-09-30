import logging
import random
import time
from datetime import datetime
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Configuración del logger
logging.basicConfig(
    filename='eventos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()
DISPOSITIVOS = ['Sensor_Temp_01', 'Sensor_Presion_02', 'Sensor_Humedad_03', 'Valvula_Entrada']

def generar_evento():
    """Genera un evento individual simulando streaming de datos."""
    evento = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dispositivo_id': random.choice(DISPOSITIVOS),
        'valor': round(random.uniform(10.0, 90.0), 2),
        'estado': random.choice(['NORMAL', 'NORMAL', 'NORMAL', 'ALERTA'])
    }
    logging.info(f"Evento emitido: {evento}")
    return evento

def procesar_lote_pandas(buffer_eventos):
    """Procesa el buffer de eventos usando Pandas."""
    df = pd.DataFrame(buffer_eventos)
    resumen = df.groupby('estado').agg(
        total_eventos=('valor', 'count'),
        promedio_valor=('valor', 'mean')
    ).reset_index()
    return df, resumen

def mostrar_tabla_rich(df):
    """Muestra los últimos eventos en formato tabla en la consola."""
    tabla = Table(title="[bold cyan]Flujo Continuo de Eventos (Kappa Stream)[/bold cyan]")
    tabla.add_column("Timestamp", style="dim")
    tabla.add_column("Dispositivo", style="bold")
    tabla.add_column("Valor", justify="right")
    tabla.add_column("Estado", justify="center")

    for _, row in df.tail(5).iterrows():
        color = "green" if row['estado'] == 'NORMAL' else "bold red"
        tabla.add_row(
            row['timestamp'],
            row['dispositivo_id'],
            f"{row['valor']:.2f}",
            f"[{color}]{row['estado']}[/{color}]"
        )
    return tabla

def ejecutar_simulacion(iteraciones=10, delay=1):
    """Ejecuta la simulación de streaming continuo."""
    console.print(Panel("[bold green]Iniciando Simulación de Arquitectura Kappa[/bold green]"))
    buffer_eventos = []

    for i in range(1, iteraciones + 1):
        evento = generar_evento()
        buffer_eventos.append(evento)
        
        df, resumen = procesar_lote_pandas(buffer_eventos)
        
        console.clear()
        console.print(mostrar_tabla_rich(df))
        console.print(f"\n[bold yellow]Eventos procesados acumulados:[/bold yellow] {len(df)}")
        time.sleep(delay)

    logging.info("Simulación finalizada correctamente.")
    console.print(Panel("[bold blue]Simulación completada con éxito[/bold blue]"))

if __name__ == '__main__':
    logging.info("Inicio de la aplicación Kappa Architecture Demo")
    ejecutar_simulacion(iteraciones=10, delay=1)