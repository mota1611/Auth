import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKENS_DIR = os.path.join(BASE_DIR, '..', 'storage', 'tokens')

if not os.path.exists(TOKENS_DIR):
    os.makedirs(TOKENS_DIR)
