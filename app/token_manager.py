import secrets
from datetime import datetime, timedelta
from app.utils import load_tokens, save_tokens

def create_token(owner_name, duration, unit):
    """Criar novo token para um dono específico."""
    tokens = load_tokens(owner_name)
    token = secrets.token_hex(32)

    if unit == "minutes":
        expiry_time = datetime.now() + timedelta(minutes=duration)
    elif unit == "hours":
        expiry_time = datetime.now() + timedelta(hours=duration)
    elif unit == "days":
        expiry_time = datetime.now() + timedelta(days=duration)
    else:
        raise ValueError("Unidade inválida: use 'minutes', 'hours' ou 'days'.")

    tokens[token] = {
        "created_at": datetime.now().isoformat(),
        "expires_at": expiry_time.isoformat(),
        "used_by": [],
        "bound_ip": None
    }
    save_tokens(owner_name, tokens)
    return token, expiry_time.isoformat()

def list_tokens():
    """Listar todos os tokens por dono."""
    return load_tokens()

def update_token_expiry(owner_name, token, duration, unit):
    """Atualizar expiração de um token existente."""
    tokens = load_tokens(owner_name)
    if token in tokens:
        if unit == "minutes":
            tokens[token]["expires_at"] = (datetime.now() + timedelta(minutes=duration)).isoformat()
        elif unit == "hours":
            tokens[token]["expires_at"] = (datetime.now() + timedelta(hours=duration)).isoformat()
        elif unit == "days":
            tokens[token]["expires_at"] = (datetime.now() + timedelta(days=duration)).isoformat()
        else:
            raise ValueError("Unidade inválida: use 'minutes', 'hours' ou 'days'.")
        save_tokens(owner_name, tokens)
        return True
    return False

def delete_token(owner_name, token):
    """Deletar token específico."""
    tokens = load_tokens(owner_name)
    if token in tokens:
        del tokens[token]
        save_tokens(owner_name, tokens)
        return True
    return False

