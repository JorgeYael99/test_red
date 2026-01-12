import time
import psutil
import speedtest  # La librería real

def verificar_wifi():
    """Verifica si WiFi está conectado"""
    try:
        interfaces = psutil.net_if_stats()
        for nombre, stats in interfaces.items():
            nombre_lower = nombre.lower()
            if any(x in nombre_lower for x in ['wi-fi', 'wireless', 'wlan']):
                return stats.isup
        return False
    except Exception as e:
        print(f"❌ Error verificando WiFi: {e}")
        return False

def hacer_test_velocidad():
    """Hace test de velocidad"""
    try:
        print("🚀 Iniciando test de velocidad...")
        st = speedtest.Speedtest()
        st.get_best_server()
        
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        
        print("\n📊 RESULTADOS:")
        print(f"⬇️ Descarga: {download:.2f} Mbps")
        print(f"⬆️ Subida: {upload:.2f} Mbps")
        print(f"🏓 Ping: {ping:.2f} ms")
        
    except Exception as e:
        print(f"❌ Error en speedtest: {e}")

# Programa principal
print("📶 Monitor WiFi + Speedtest")
print("---------------------------")

try:
    while True:
        hora = time.strftime("%H:%M:%S")
        
        if verificar_wifi():
            print(f"[{hora}] ✅ WiFi CONECTADO")
            hacer_test_velocidad()
            print("\n⏳ Esperando 5 segundos...")
            time.sleep(5)
        else:
            print(f"[{hora}] ❌ WiFi DESCONECTADO")
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\n👋 Programa terminado")