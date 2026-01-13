import time
import psutil
import speedtest  # La librería real
import traceback

def verificar_wifi():
    """Verifica si HAY RED (cualquiera) y muestra nombres"""
    try:
        interfaces = psutil.net_if_stats()
        # IMPRIMIR QUÉ ENCUENTRA PARA DEPURAR
        print(f"\n🔍 DEBUG - Interfaces encontradas: {list(interfaces.keys())}")
        
        for nombre, stats in interfaces.items():
            # Si quieres que funcione en tu servidor, agrega 'eth' o 'en' a la lista
            # o simplemente devuelve True si encuentras alguna interfaz UP que no sea 'lo'
            nombre_lower = nombre.lower()
            
            # Agregamos filtros comunes de cable (eth, enp, ens)
            filtros = ['wi-fi', 'wireless', 'wlan', 'eth', 'enp', 'ens']
            
            if any(x in nombre_lower for x in filtros):
                if stats.isup:
                    return True
        return False
    except Exception as e:
        print(f"❌ Error verificando Red: {e}")
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
            traceback.print_exc()
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\n👋 Programa terminado")
