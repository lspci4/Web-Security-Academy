import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxie_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, login_url):
    
    response = session.get(login_url, verify=False, proxies=proxie_setting)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find("input",{"name": "csrf"})['value']
    print(csrf_token)
    return csrf_token
        
def api_key_user(session, base_url):
    """Login user wiener"""
    login_url = f"{base_url}/login"
    csrf_token = get_csrf_token(session, login_url)
    data_credential = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }
    response = session.post(login_url, data=data_credential, verify=False, proxies=proxie_setting)
    if "Log out" in response.text:
        print("[+] Login exitoso")
    else:
        print("[-] Login fallido")

def main():
    if len(sys.argv) !=2:
        print(f"[+] {sys.argv[0]} <url>")
        print(f"[+] Uso: {sys.argv[0]} www.example.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    api_key_user(session, base_url)

if __name__ == "__main__":
    main()