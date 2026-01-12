import time
import speedtest
import logging
from datetime import datetime

# Configurar el sistema de registros (Logs)
# Esto guardará todo en un archivo llamado 'mi_registro.log'
logging.basicConfig(
    filename='mi_registro.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def hacer_test_automatico():
    try:
        logging.info("🚀 Iniciando test de velocidad automático...")
        
        st = speedtest.Speedtest()
        
        logging.info("🔍 Buscando mejor servidor...")
        st.get_best_server()
        
        logging.info("📥 Probando descarga...")
        download = st.download() / 1_000_000
        
        logging.info("📤 Probando subida...")
        upload = st.upload() / 1_000_000
        
        ping = st.results.ping
        
        resultado = f"RESULTADO: Descarga: {download:.2f} Mbps | Subida: {upload:.2f} Mbps | Ping: {ping:.2f} ms"
        print(resultado) # Esto saldrá en consola si la tienes abierta
        logging.info(resultado) # Esto se guarda en el archivo
        
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    print("El programa se está ejecutando en segundo plano. Revisa 'mi_registro.log'.")
    while True:
        hacer_test_automatico()
        # Esperar 1 hora (3600 segundos) antes del siguiente test
        # O cambia esto al tiempo que desees
        time.sleep(3600)