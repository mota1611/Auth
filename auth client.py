import requests
import sys
import os
import socket
import uuid
import json
from platform import system, release, version

AUTH_DIR = "C:\\Automação"
AUTH_FILE = os.path.join(AUTH_DIR, "auth.json")
SERVER_URL = "http://4.228.61.93:5000/validate"


def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 2 * 6, 8)][::-1])
    return mac


def load_token():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as file:
            data = json.load(file)
            return data.get("token")
    return None


def save_token(token):
    if not os.path.exists(AUTH_DIR):
        os.makedirs(AUTH_DIR)
    with open(AUTH_FILE, "w") as file:
        json.dump({"token": token}, file, indent=4)


def remove_token():
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)


def get_token():
    token = load_token()
    if not token:
        print("Token não encontrado. Por favor, insira seu token de autenticação:")
        token = input("Token: ").strip()
        save_token(token)
    return token


def check_server(token):
    try:
        user_name = os.getenv("USERNAME", os.getenv("USER", "Desconhecido")) 
        local_ip = socket.gethostbyname(socket.gethostname())  
        hostname = socket.gethostname()  
        mac_address = get_mac_address()  
        os_info = f"{system()} {release()} ({version()})"

        headers = {
            "Authorization": token,
            "User-Name": user_name,
            "Local-IP": local_ip,
            "MAC-Address": mac_address,
            "Hostname": hostname,
            "OS-Info": os_info
        }

        response = requests.post(SERVER_URL, headers=headers, timeout=10)

        if response.status_code == 200 and response.json().get("status") == "active":
            print("Servidor ativo e token válido. Continuando a execução.")
        elif response.status_code == 403:
            print("Token expirado ou bloqueado. Solicitando novo token.")
            remove_token() 
            sys.exit(1)  
        else:
            print(f"Erro no servidor: {response.status_code}. Detalhes: {response.json().get('message', 'Servidor inativo ou resposta inválida.')}")
            sys.exit(1)
    except requests.exceptions.Timeout:
        print("Erro: O servidor demorou muito para responder. Verifique sua conexão ou tente novamente.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao servidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    token = get_token()  
    check_server(token) 
