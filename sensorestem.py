import logging
import random
import time
from datetime import datetime
import pandas as pd

# Configuración del logger
logging.basicConfig(
    filename='eventos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

if __name__ == '__main__':
    logging.info("Inicio de la aplicación Kappa Architecture Demo")
    print("Inicializando componentes de la arquitectura Kappa...")
