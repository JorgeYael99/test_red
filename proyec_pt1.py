import time
import psutil
import speedtest
import socket

def obtener_info_red():
    """Obtiene información de la red WiFi conectada"""
    try:
        # Obtener direcciones de red
        hostname = socket.gethostname()
        direccion_ip = socket.gethostbyname(hostname)
        
        # Obtener interfaz WiFi activa
        interfaces = psutil.nent_if_addrs()
        stats = psutil.net_if_stats()
        
        for nombre, direcciones in interfaces.items():
            nombre_lower = nombre.lower()
            if any(x in nombre_lower for x in ['wi-fi', 'wireless', 'wlan']):
                if stats[nombre].isup:
                    # Obtener dirección MAC
                    mac_address = ""
                    for direccion in direcciones:
                        if direccion.family == psutil.AF_LINK:
                            mac_address = direccion.address
                            break
                    
                    # Intentar obtener el SSID (nombre de la red WiFi)
                    ssid = "Desconocido"
                    try:
                        # En Windows, podemos intentar obtener el SSID
                        import subprocess
                        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                              capture_output=True, text=True, encoding='latin-1')
                        for line in result.stdout.split('\n'):
                            if 'SSID' in line and 'BSSID' not in line:
                                ssid = line.split(':')[-1].strip()
                                break
                    except:
                        ssid = nombre  # Usar el nombre de la interfaz como fallback
                    
                    return {
                        'conectado': True,
                        'interfaz': nombre,
                        'ssid': ssid,
                        'ip': direccion_ip,
                        'mac': mac_address
                    }
        
        return {'conectado': False}
        
    except Exception as e:
        print(f"❌ Error obteniendo información de red: {e}")
        return {'conectado': False}

def hacer_test_velocidad():
    """Hace test de velocidad"""
    try:
        print("🚀 Iniciando test de velocidad...")
        print("⏳ Buscando mejor servidor...")
        st = speedtest.Speedtest()
        st.get_best_server()
        
        print("📥 Probando velocidad de descarga...")
        download = st.download() / 1_000_000
        
        print("📤 Probando velocidad de subida...")
        upload = st.upload() / 1_000_000
        
        ping = st.results.ping
        
        print("\n" + "="*50)
        print("📊 RESULTADOS DEL TEST DE VELOCIDAD")
        print("="*50)
        print(f"⬇️  Descarga: {download:.2f} Mbps")
        print(f"⬆️  Subida: {upload:.2f} Mbps")
        print(f"🏓 Ping: {ping:.2f} ms")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en speedtest: {e}")
        return False

def preguntar_repetir():
    """Pregunta al usuario si quiere repetir el test"""
    while True:
        respuesta = input("\n¿Desea realizar otro test? (y/n): ").lower().strip()
        if respuesta in ['y', 'yes', 's', 'si', 'sí']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        else:
            print("❌ Por favor, ingrese 'y' para sí o 'n' para no")

def main():
    """Función principal del programa"""
    print("📶 Monitor WiFi + Speedtest")
    print("="*40)
    
    while True:
        hora = time.strftime("%H:%M:%S")
        
        # Paso 1: Detectar si está conectada o desconectada
        info_red = obtener_info_red()
        
        if info_red['conectado']:
            print(f"\n[{hora}] ✅ WiFi CONECTADO")
            
            # Paso 2: Mostrar información de la red
            print("\n🌐 INFORMACIÓN DE LA RED:")
            print(f"   • Red WiFi: {info_red['ssid']}")
            print(f"   • Interfaz: {info_red['interfaz']}")
            print(f"   • Dirección IP: {info_red['ip']}")
            print(f"   • Dirección MAC: {info_red['mac']}")
            
            # Paso 3: Iniciar test de velocidad
            print("\n" + "-"*40)
            exito_test = hacer_test_velocidad()
            
            # Paso 4: Los resultados ya se muestran en la función hacer_test_velocidad()
            
            # Paso 5: Preguntar si quiere repetir
            if not preguntar_repetir():
                print("\n👋 Programa terminado. ¡Hasta luego!")
                break
            else:
                print("\n" + "="*40)
                print("🔄 Reiniciando test...")
                print("="*40)
                
        else:
            print(f"[{hora}] ❌ WiFi DESCONECTADO")
            print("💡 Conecte a una red WiFi y espere...")
            time.sleep(3)  # Esperar 3 segundos antes de revisar nuevamente

# Ejecutar el programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

        """"""