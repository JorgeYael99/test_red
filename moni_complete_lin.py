import time
import psutil
import speedtest
import socket
import sys
import subprocess

def obtener_info_red():
    """Obtiene información de la red conectada (Cable o WiFi)"""
    try:
        # Obtener direcciones de red
        hostname = socket.gethostname()
        try:
            direccion_ip = socket.gethostbyname(hostname)
        except:
            direccion_ip = "127.0.0.1"
        
        # Obtener interfaces
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        # 1. FILTROS ACTUALIZADOS PARA TU SERVIDOR (Cable + WiFi + VPN)
        filtros = ['wi-fi', 'wireless', 'wlan', 'eth', 'enp', 'ens', 'tailscale']

        for nombre, direcciones in interfaces.items():
            nombre_lower = nombre.lower()
            
            # Buscamos si el nombre coincide con algun filtro
            if any(x in nombre_lower for x in filtros):
                # Verificamos si existe en stats y está activa (ISUP)
                if nombre in stats and stats[nombre].isup:
                    
                    # Obtener dirección MAC
                    mac_address = "No disponible"
                    for direccion in direcciones:
                        if direccion.family == psutil.AF_LINK:
                            mac_address = direccion.address
                            break
                    
                    # 2. LOGICA DE NOMBRE DE RED (SSID)
                    ssid = nombre # Por defecto usamos el nombre de la interfaz (ej: enp0s3)
                    
                    # Si es Windows intentamos sacar el nombre del WiFi
                    if sys.platform == 'win32' and 'wi-fi' in nombre_lower:
                        try:
                            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                                    capture_output=True, text=True, encoding='latin-1')
                            for line in result.stdout.split('\n'):
                                if 'SSID' in line and 'BSSID' not in line:
                                    ssid = line.split(':')[-1].strip()
                                    break
                        except:
                            pass
                    # Si estamos en Linux y no es WiFi, lo llamamos Cableado
                    elif 'eth' in nombre_lower or 'enp' in nombre_lower:
                        ssid = "Cable / Ethernet"
                    
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
    # Asegurar que porcentaje esté entre 0 y 100
    porcentaje = max(0, min(100, porcentaje))
    completado = int(ancho * porcentaje / 100)
    restante = ancho - completado
    barra = f"[{'█' * completado}{'░' * restante}]"
    porcentaje_texto = f"{porcentaje:.1f}%".rjust(6)
    print(f"\r{etapa} {barra} {porcentaje_texto}", end='', flush=True)
    
    if porcentaje >= 100:
        print()  # Nueva línea al completar

def hacer_test_velocidad():
    """Hace test de velocidad con barras de progreso simuladas (Más estable)"""
    try:
        print("🚀 Iniciando test de velocidad...")
        print()
        
        st = speedtest.Speedtest()
        
        # Etapa 1: Buscar mejor servidor
        print("🔍 Buscando mejor servidor...")
        for i in range(101):
            if i == 50: 
                st.get_best_server()
            mostrar_progreso("Configura:", i, 30)
            time.sleep(0.01)
        
        print("✅ Servidor encontrado")
        time.sleep(0.5)
        
        # Etapa 2: Velocidad de descarga
        print("\n📥 Probando velocidad de descarga...")
        download_result = 0
        
        # Simular progreso mientras descarga de fondo
        # Nota: speedtest bloquea el hilo, asi que esto es una simulación visual
        # antes de la llamada real para dar feedback al usuario
        for i in range(1, 40):
             mostrar_progreso("Descarga:", i, 30)
             time.sleep(0.02)
        
        # Ejecución real (puede tardar unos segundos donde la barra se detiene)
        download_result = st.download() 
        
        # Completar barra
        for i in range(40, 101):
            mostrar_progreso("Descarga:", i, 30)
            time.sleep(0.005)

        download = download_result / 1_000_000
        print("✅ Descarga completada")
        
        # Etapa 3: Velocidad de subida
        print("\n📤 Probando velocidad de subida...")
        
        # Simulación inicial
        for i in range(1, 40):
             mostrar_progreso("Subida:   ", i, 30)
             time.sleep(0.02)
             
        upload_result = st.upload()
        
        # Completar barra
        for i in range(40, 101):
            mostrar_progreso("Subida:   ", i, 30)
            time.sleep(0.005)

        upload = upload_result / 1_000_000
        print("✅ Subida completada")
        
        ping = st.results.ping
        
        # Mostrar resultados finales
        print("\n" + "="*50)
        print("📊 RESULTADOS DEL TEST DE VELOCIDAD")
        print("="*50)
        print(f"⬇️  Descarga: {download:.2f} Mbps")
        print(f"⬆️  Subida:   {upload:.2f} Mbps")
        print(f"🏓 Ping:     {ping:.2f} ms")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"\n❌ Error en speedtest: {e}")
        return False

def hacer_test_velocidad_real():
    """Versión con callbacks para speedtest"""
    try:
        print("🚀 Iniciando test de velocidad (Modo Real)...")
        st = speedtest.Speedtest()
        
        # Variables de estado
        descarga_done = False
        subida_done = False

        # Callbacks simplificados
        def callback_descarga(current, total, start=False, end=False):
            nonlocal descarga_done
            if total > 0:
                p = (current / total) * 100
                mostrar_progreso("Descarga:", p, 30)
            if end: descarga_done = True

        def callback_subida(current, total, start=False, end=False):
            nonlocal subida_done
            if total > 0:
                p = (current / total) * 100
                mostrar_progreso("Subida:   ", p, 30)
            if end: subida_done = True

        print("🔍 Buscando servidor...")
        st.get_best_server()
        print("✅ Servidor encontrado\n")

        print("📥 Iniciando descarga...")
        try:
            # Intentamos usar callbacks si la librería lo soporta
            d = st.download(callback=callback_descarga)
        except TypeError:
             # Fallback si la versión instalada de speedtest es vieja y no soporta callbacks
             print("   (Tu versión de speedtest no soporta callbacks visuales, espera...)")
             d = st.download()
        
        if not descarga_done: mostrar_progreso("Descarga:", 100, 30)
        print("\n✅ Completado\n")

        print("📤 Iniciando subida...")
        try:
            u = st.upload(callback=callback_subida)
        except TypeError:
             print("   (Calculando subida, espera...)")
             u = st.upload()

        if not subida_done: mostrar_progreso("Subida:   ", 100, 30)
        print("\n✅ Completado")

        # Resultados
        print("\n" + "="*50)
        print(f"⬇️  Descarga: {d / 1_000_000:.2f} Mbps")
        print(f"⬆️  Subida:   {u / 1_000_000:.2f} Mbps")
        print(f"🏓 Ping:     {st.results.ping:.2f} ms")
        print("="*50)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("📶 Monitor de Red Avanzado (Server Edition)")
    print("===========================================")
    
    while True:
        hora = time.strftime("%H:%M:%S")
        info = obtener_info_red()
        
        if info['conectado']:
            print(f"\n[{hora}] ✅ RED CONECTADA")
            print(f"   • Tipo/SSID: {info['ssid']}")
            print(f"   • Interfaz:  {info['interfaz']}")
            print(f"   • IP Local:  {info['ip']}")
            
            print("\n¿Qué deseas hacer?")
            print("1. Test Rápido (Visual simulado)")
            print("2. Test Preciso (Callbacks reales)")
            print("3. Salir")
            
            opcion = input("\nOpción > ").strip()
            
            if opcion == "3":
                print("👋 ¡Hasta luego!")
                break
            elif opcion == "2":
                hacer_test_velocidad_real()
            else:
                hacer_test_velocidad()
                
            # Pausa antes de repetir
            input("\nPresiona ENTER para volver al menú...")
            
        else:
            print(f"[{hora}] ❌ RED DESCONECTADA (Buscando interfaces cable/wifi...)")
            time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Programa interrumpido")