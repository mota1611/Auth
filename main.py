import os
from app.token_manager import create_token, update_token_expiry, delete_token, list_tokens
from app.server import start_server
import threading

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_owner_and_token():
    tokens = list_tokens()
    if not tokens:
        print("Nenhum token encontrado.")
        input("Pressione Enter para voltar ao menu...")
        return None, None

    print("Donos disponíveis:")
    owner_names = list(tokens.keys())
    for idx, owner in enumerate(owner_names, start=1):
        print(f"{idx}. {owner}")

    owner_choice = input("Escolha o número do dono (ou 0 para voltar): ")
    if owner_choice == "0":
        return None, None

    try:
        owner_choice = int(owner_choice) - 1
        owner_name = owner_names[owner_choice]

        print(f"Tokens para o dono {owner_name}:")
        token_list = list(tokens[owner_name].keys())
        for idx, token in enumerate(token_list, start=1):
            print(f"{idx}. {token}")

        token_choice = input("Escolha o número do token (ou 0 para voltar): ")
        if token_choice == "0":
            return None, None

        token_choice = int(token_choice) - 1
        token = token_list[token_choice]
        return owner_name, token
    except (ValueError, IndexError):
        print("Opção inválida.")
        input("Pressione Enter para voltar ao menu...")
        return None, None

def main():
    while True:
        clear_console()
        print("\n===== Gerenciador de Tokens =====")
        print("1. Criar novo token")
        print("2. Alterar expiração de um token")
        print("3. Deletar token")
        print("4. Listar tokens")
        print("5. Iniciar servidor")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            owner_name = input("Nome do dono: ")

            print("\nEscolha a unidade de tempo:")
            print("1. Minutos")
            print("2. Horas")
            print("3. Dias")
            unit_choice = input("Digite o número da unidade (1/2/3): ")
            if unit_choice == "1":
                unit = "minutes"
            elif unit_choice == "2":
                unit = "hours"
            elif unit_choice == "3":
                unit = "days"
            else:
                print("Unidade inválida.")
                input("Pressione Enter para continuar...")
                continue

            try:
                duration = int(input(f"Digite a duração em {unit}: "))
            except ValueError:
                print("Erro: A duração deve ser um número inteiro.")
                input("Pressione Enter para continuar...")
                continue

            token, expiry = create_token(owner_name, duration, unit)
            print(f"\nToken criado com sucesso!")
            print(f"Token: {token}")
            print(f"Expira em: {expiry}")
            input("\nPressione Enter para continuar...")

        elif choice == "2":
            owner_name, token = select_owner_and_token()
            if not owner_name or not token:
                continue

            print("\nEscolha a nova unidade de tempo:")
            print("1. Minutos")
            print("2. Horas")
            print("3. Dias")
            unit_choice = input("Digite o número da unidade (1/2/3): ")
            if unit_choice == "1":
                unit = "minutes"
            elif unit_choice == "2":
                unit = "hours"
            elif unit_choice == "3":
                unit = "days"
            else:
                print("Unidade inválida.")
                input("Pressione Enter para continuar...")
                continue

            try:
                duration = int(input(f"Digite a nova duração em {unit}: "))
            except ValueError:
                print("Erro: A duração deve ser um número inteiro.")
                input("Pressione Enter para continuar...")
                continue

            if update_token_expiry(owner_name, token, duration, unit):
                print("Expiração do token atualizada com sucesso.")
            else:
                print("Erro ao atualizar a expiração do token.")
            input("Pressione Enter para continuar...")

        elif choice == "3":
            owner_name, token = select_owner_and_token()
            if not owner_name or not token:
                continue

            if delete_token(owner_name, token):
                print("Token deletado com sucesso.")
            else:
                print("Erro ao deletar o token.")
            input("Pressione Enter para continuar...")

        elif choice == "4":
            tokens = list_tokens()
            if not tokens:
                print("Nenhum token encontrado.")
            else:
                for owner, token_data in tokens.items():
                    print(f"\nDono: {owner}")
                    for token, details in token_data.items():
                        print(f"  Token: {token}")
                        print(f"    Criado em: {details['created_at']}")
                        print(f"    Expira em: {details['expires_at']}")
                        print(f"    IP vinculado: {details.get('bound_ip', 'Nenhum')}")
                        print("    Histórico de uso:")
                        for usage in details["used_by"]:
                            print(f"      - IP: {usage['ip']}, Usado em: {usage['used_at']}")
            input("\nPressione Enter para continuar...")

        elif choice == "5":
            threading.Thread(target=start_server, daemon=True).start()
            input("Servidor iniciado. Pressione Enter para voltar ao menu...")

        elif choice == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
