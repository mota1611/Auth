import os
import json
from config.settings import TOKENS_DIR

def load_tokens(owner_name=None):
    """Carrega tokens para um dono específico ou todos os tokens."""
    tokens = {}
    if owner_name:
        filepath = os.path.join(TOKENS_DIR, f"{owner_name}Token.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                tokens = json.load(file)
    else:
        for filename in os.listdir(TOKENS_DIR):
            if filename.endswith("Token.json"):
                owner_name = filename.replace("Token.json", "")
                filepath = os.path.join(TOKENS_DIR, filename)
                with open(filepath, "r") as file:
                    tokens[owner_name] = json.load(file)
    return tokens

def save_tokens(owner_name, tokens):
    """Salva os tokens no arquivo JSON do respectivo dono."""
    filepath = os.path.join(TOKENS_DIR, f"{owner_name}Token.json")
    with open(filepath, "w") as file:
        json.dump(tokens, file, indent=4)

def delete_token(owner_name, token):
    """Deleta um token específico de um dono."""
    tokens = load_tokens(owner_name)
    if token in tokens:
        del tokens[token]
        save_tokens(owner_name, tokens)
        return True
    return False
