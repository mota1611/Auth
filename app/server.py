import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from app.utils import load_tokens, save_tokens, delete_token

app = Flask(__name__, template_folder="")

TOKENS_DIR = "storage/tokens"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/tokens', methods=['GET'])
def list_all_tokens():
    """Lista todos os arquivos de tokens disponíveis."""
    token_files = [
        filename for filename in os.listdir(TOKENS_DIR) if filename.endswith("Token.json")
    ]

    if token_files:
        return render_template("tokens_list.html", token_files=token_files)
    else:
        return "<h1>Nenhum arquivo de token disponível.</h1>", 404

@app.route('/tokens/view/<filename>', methods=['GET'])
def view_token_file(filename):
    filepath = os.path.join(TOKENS_DIR, filename)

    if os.path.exists(filepath) and filename.endswith("Token.json"):
        with open(filepath, "r") as file:
            tokens = json.load(file)
        return render_template("token_details.html", filename=filename, tokens=tokens)
    else:
        return f"<h1>Arquivo {filename} não encontrado.</h1>", 404

@app.route('/tokens/<ip>', methods=['GET'])
def view_tokens(ip):
    tokens_data = {}

    for filename in os.listdir(TOKENS_DIR):
        if filename.endswith("Token.json"):
            owner_name = filename.replace("Token.json", "")
            filepath = os.path.join(TOKENS_DIR, filename)

            with open(filepath, "r") as file:
                owner_tokens = json.load(file)

                tokens = {
                    token: details for token, details in owner_tokens.items()
                    if details.get("bound_ip") == ip
                }

                if tokens:
                    tokens_data[owner_name] = tokens

    if tokens_data:
        return render_template("ip_tokens.html", ip=ip, tokens_data=tokens_data)
    else:
        return f"<h1>Nenhum token encontrado para o IP {ip}.</h1>", 404

@app.route('/validate', methods=['POST'])
def validate():
    token = request.headers.get("Authorization")
    client_ip = request.remote_addr

    print(f"Token recebido: {token}")
    tokens = load_tokens()
    print(f"Tokens carregados: {tokens}")

    for owner, owner_tokens in tokens.items():
        if token in owner_tokens:
            token_data = owner_tokens[token]

            current_time = datetime.now()
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            print(f"Current time: {current_time}, Expires at: {expires_at}")

            if current_time > expires_at:
                delete_token(owner, token)
                print("Token expirado.")
                return jsonify({"status": "expired", "message": "Token expirado."}), 403

            if not token_data.get("bound_ip"):
                token_data["bound_ip"] = client_ip
            elif token_data["bound_ip"] != client_ip:
                print("Token já vinculado a outro IP.")
                return jsonify({
                    "status": "blocked",
                    "message": "Token já vinculado a outro IP."
                }), 403

            updated = False
            for usage in token_data["used_by"]:
                if usage["ip"] == client_ip:
                    usage["used_at"] = datetime.now().isoformat()
                    updated = True
                    break

            if not updated:
                token_data["used_by"].append({
                    "ip": client_ip,
                    "used_at": datetime.now().isoformat()
                })

            save_tokens(owner, owner_tokens)
            print("Token válido.")
            return jsonify({"status": "active", "message": "Token válido."}), 200

    print("Token não encontrado.")
    return jsonify({"status": "invalid", "message": "Token inválido ou não encontrado."}), 403

def start_server():
    print("Servidor iniciado em http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    start_server()
