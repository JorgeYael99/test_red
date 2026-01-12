import time
import psutil
import speedtest
import socket
import sys

def obtener_info_red():
    """Obtiene información de la red WiFi conectada"""
    try:
        # Obtener direcciones de red
        hostname = socket.gethostname()
        direccion_ip = socket.gethostbyname(hostname)
        
        # Obtener interfaz WiFi activa
        interfaces = psutil.net_if_addrs()
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

def mostrar_progreso(etapa, porcentaje, ancho=40):
    """Muestra una barra de progreso visual"""
    completado = int(ancho * porcentaje / 100)
    restante = ancho - completado
    barra = f"[{'█' * completado}{'░' * restante}]"
    porcentaje_texto = f"{porcentaje:.1f}%".rjust(6)
    print(f"\r{etapa} {barra} {porcentaje_texto}", end='', flush=True)
    
    if porcentaje >= 100:
        print()  # Nueva línea al completar

def hacer_test_velocidad():
    """Hace test de velocidad con barras de progreso simuladas"""
    try:
        print("🚀 Iniciando test de velocidad...")
        print()
        
        st = speedtest.Speedtest()
        
        # Etapa 1: Buscar mejor servidor
        print("🔍 Buscando mejor servidor...")
        for i in range(101):
            if i == 50:  # Simular que a la mitad encuentra el servidor
                st.get_best_server()
            mostrar_progreso("Progreso:", i, 30)
            time.sleep(0.02)
        
        print("✅ Mejor servidor encontrado")
        time.sleep(0.5)
        
        # Etapa 2: Velocidad de descarga
        print("\n📥 Probando velocidad de descarga...")
        download_result = 0
        
        # Simular progreso de descarga
        for i in range(101):
            if i == 30:
                # Iniciar la descarga real en un punto específico
                download_result = st.download()
            mostrar_progreso("Descarga:", i, 30)
            # Hacer la animación más realista (más lento al final)
            if i < 80:
                time.sleep(0.03)
            elif i < 95:
                time.sleep(0.05)
            else:
                time.sleep(0.1)
        
        download = download_result / 1_000_000
        print("✅ Descarga completada")
        time.sleep(0.5)
        
        # Etapa 3: Velocidad de subida
        print("\n📤 Probando velocidad de subida...")
        upload_result = 0
        
        # Simular progreso de subida
        for i in range(101):
            if i == 25:
                # Iniciar la subida real
                upload_result = st.upload()
            mostrar_progreso("Subida:  ", i, 30)
            # Hacer la animación más realista
            if i < 70:
                time.sleep(0.04)
            elif i < 90:
                time.sleep(0.06)
            else:
                time.sleep(0.15)
        
        upload = upload_result / 1_000_000
        print("✅ Subida completada")
        time.sleep(0.5)
        
        # Obtener ping
        ping = st.results.ping
        
        # Mostrar resultados finales
        print("\n" + "="*50)
        print("📊 RESULTADOS DEL TEST DE VELOCIDAD")
        print("="*50)
        print(f"⬇️  Descarga: {download:.2f} Mbps")
        print(f"⬆️  Subida: {upload:.2f} Mbps")
        print(f"🏓 Ping: {ping:.2f} ms")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en speedtest: {e}")
        return False

def hacer_test_velocidad_real():
    """Versión con callbacks corregidos para la librería speedtest"""
    try:
        print("🚀 Iniciando test de velocidad...")
        print()
        
        st = speedtest.Speedtest()
        
        # Variables para trackear progreso
        descarga_completada = False
        subida_completada = False
        
        # Callbacks corregidos - deben aceptar los parámetros que envía speedtest
        def progreso_descarga(current, total, start=False, end=False):
            nonlocal descarga_completada
            if start:
                print("📥 Iniciando descarga...")
                return
            if end:
                descarga_completada = True
                mostrar_progreso("Descarga:", 100, 30)
                return
            if total > 0:
                porcentaje = (current / total) * 100
                mostrar_progreso("Descarga:", min(porcentaje, 99), 30)
        
        def progreso_subida(current, total, start=False, end=False):
            nonlocal subida_completada
            if start:
                print("📤 Iniciando subida...")
                return
            if end:
                subida_completada = True
                mostrar_progreso("Subida:  ", 100, 30)
                return
            if total > 0:
                porcentaje = (current / total) * 100
                mostrar_progreso("Subida:  ", min(porcentaje, 99), 30)
        
        # Etapa 1: Buscar servidor
        print("🔍 Buscando mejor servidor...")
        for i in range(101):
            if i == 50:
                try:
                    st.get_best_server()
                except:
                    pass
            mostrar_progreso("Servidor:", i, 30)
            time.sleep(0.01)
        print("\n✅ Servidor encontrado")
        time.sleep(0.5)
        
        # Etapa 2: Descarga con progreso real
        print("\n📥 Probando velocidad de descarga...")
        try:
            download = st.download(callback=progreso_descarga) / 1_000_000
            if not descarga_completada:
                mostrar_progreso("Descarga:", 100, 30)
            print("\n✅ Descarga completada")
        except Exception as e:
            print(f"\n❌ Error en descarga: {e}")
            return False
        
        time.sleep(0.5)
        
        # Etapa 3: Subida con progreso real
        print("\n📤 Probando velocidad de subida...")
        try:
            upload = st.upload(callback=progreso_subida) / 1_000_000
            if not subida_completada:
                mostrar_progreso("Subida:  ", 100, 30)
            print("\n✅ Subida completada")
        except Exception as e:
            print(f"\n❌ Error en subida: {e}")
            return False
        
        ping = st.results.ping
        
        # Resultados
        print("\n" + "="*50)
        print("📊 RESULTADOS DEL TEST DE VELOCIDAD")
        print("="*50)
        print(f"⬇️  Descarga: {download:.2f} Mbps")
        print(f"⬆️  Subida: {upload:.2f} Mbps")
        print(f"🏓 Ping: {ping:.2f} ms")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en speedtest: {e}")
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
    print("📶 Monitor WiFi + Speedtest con Progreso Visual")
    print("="*50)
    
    while True:
        hora = time.strftime("%H:%M:%S")
        
        # Paso 1: Detectar conexión
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
            print("\n" + "-"*50)
            
            # Preguntar qué versión del test prefiere
            print("\n¿Qué tipo de test desea realizar?")
            print("1. Test con progreso visual (recomendado)")
            print("2. Test con progreso real (más preciso)")
            
            opcion = input("Seleccione (1/2): ").strip()
            
            if opcion == "2":
                print("\n⚠️  Modo real seleccionado (puede mostrar errores de callback)")
                exito_test = hacer_test_velocidad_real()
            else:
                exito_test = hacer_test_velocidad()
            
            # Paso 5: Preguntar si quiere repetir
            if not preguntar_repetir():
                print("\n👋 Programa terminado. ¡Hasta luego!")
                break
            else:
                print("\n" + "="*50)
                print("🔄 Reiniciando test...")
                print("="*50)
                
        else:
            print(f"[{hora}] ❌ WiFi DESCONECTADO")
            print("💡 Conecte a una red WiFi y espere...")
            time.sleep(3)

# Ejecutar el programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")