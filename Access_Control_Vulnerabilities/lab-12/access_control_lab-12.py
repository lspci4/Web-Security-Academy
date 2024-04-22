import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) !=2:
        print(f"(+) Uso: {sys.argv[0]} <url>")
        print(f"(+) Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    upgrade_user(session,base_url)

def upgrade_user(session,base_url):
    login_url = f"{base_url}/login"
    credential = {'username': 'wiener','password': 'peter'}
    response = session.post(login_url,data=credential,verify=False,proxies=proxies_setting)
    if "Log out" in response.text:
        print(f"(+) Login exitoso como user wiener")
    else:
        print(f"(-) Login fallido para el user wiener")

    
if __name__ == "__main__":
    main()
