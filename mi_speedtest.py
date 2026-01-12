import speedtest

def hacer_test_velocidad():
    """Función para hacer test de velocidad"""
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
        
        return download, upload, ping
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None

# ✅ AGREGAR ESTO AL FINAL PARA PRUEBAS
if __name__ == "__main__":
    hacer_test_velocidad()