import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(s, url):
    path = '/administrator-panel/delete?username=carlos'
    

def main():
    if (len(sys.argv[0]))!=2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com")
        return
    
    url = sys.argv[1]
    s = requests.session()
    delete_user(s, url)
    

if __name__ == "__main__":
    main()