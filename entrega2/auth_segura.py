import json
import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

ARQUIVO_DB = "usuarios_db.json"

ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)


def carregar_banco() -> dict:
    if not os.path.exists(ARQUIVO_DB):
        return {}
    with open(ARQUIVO_DB, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_banco(dados: dict) -> None:
    with open(ARQUIVO_DB, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def cadastrar_usuario(usuario: str, senha: str) -> bool:
    db = carregar_banco()
    if usuario in db:
        print(f"[ERRO] O usuário '{usuario}' já está cadastrado.")
        return False

    hash_armazenado = ph.hash(senha)

    db[usuario] = {
        "algoritmo": "Argon2id",
        "hash_completo": hash_armazenado
    }
    salvar_banco(db)
    print(f"[SUCESSO] Usuário '{usuario}' cadastrado com proteção Argon2id!")
    return True


def autenticar_usuario(usuario: str, senha_fornecida: str) -> bool:
    db = carregar_banco()
    registro = db.get(usuario)

    if not registro:
        print(f"[FALHA] Autenticação negada para '{usuario}' (usuário ou senha inválidos).")
        return False

    hash_salvo = registro["hash_completo"]

    try:
        ph.verify(hash_salvo, senha_fornecida)

        if ph.check_needs_rehash(hash_salvo):
            db[usuario]["hash_completo"] = ph.hash(senha_fornecida)
            salvar_banco(db)

        print(f"[SUCESSO] Login aprovado para '{usuario}'!")
        return True

    except VerifyMismatchError:
        print(f"[FALHA] Autenticação negada para '{usuario}': senha incorreta.")
        return False
    except (VerificationError, InvalidHashError) as e:
        print(f"[ERRO CRÍTICO] Falha na verificação do hash: {e}")
        return False


def exibir_registro_protegido(usuario: str) -> None:
    db = carregar_banco()
    registro = db.get(usuario)
    if not registro:
        print(f"Usuário '{usuario}' não encontrado no banco.")
        return

    hash_str = registro["hash_completo"]
    partes = hash_str.split("$")
    print("\n--- EVIDÊNCIA DE ARMAZENAMENTO SEGURO (BANCO DE DADOS) ---")
    print(f"Usuário      : {usuario}")
    print(f"Hash PHC     : {hash_str}")
    if len(partes) >= 6:
        print(f"Algoritmo    : {partes[1]} (versão {partes[2]})")
        print(f"Parâmetros   : {partes[3]}")
        print(f"Salt (Base64): {partes[4]}")
        print(f"Hash (Base64): {partes[5]}")
    print("----------------------------------------------------------\n")


def executar_demonstracao_automatica() -> None:
    print("\n=== INICIANDO DEMONSTRAÇÃO AUTOMÁTICA (ENTREGA 2) ===\n")
    if os.path.exists(ARQUIVO_DB):
        os.remove(ARQUIVO_DB)

    usuario_teste = "AlunoDeSeguranca"
    senha_correta = "SenhaForte@Unit2026!"
    senha_errada = "SenhaErrada123"

    print("1. Cadastrando usuário de teste...")
    cadastrar_usuario(usuario_teste, senha_correta)

    print("\n2. Inspecionando registro salvo (sem senha em texto puro)...")
    exibir_registro_protegido(usuario_teste)

    print("3. Testando login com a SENHA CORRETA...")
    autenticar_usuario(usuario_teste, senha_correta)

    print("\n4. Testando login com a SENHA INCORRETA...")
    autenticar_usuario(usuario_teste, senha_errada)

    print("\n=== DEMONSTRAÇÃO CONCLUÍDA ===\n")


def menu() -> None:
    while True:
        print("=== SISTEMA DE AUTENTICAÇÃO SEGURA (ARGON2ID) ===")
        print("1. Cadastrar novo usuário")
        print("2. Realizar login")
        print("3. Inspecionar hash/salt armazenado de um usuário")
        print("4. Executar bateria de testes completa (Demonstração)")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            usuario = input("Novo usuário: ").strip()
            senha = input("Senha: ")
            cadastrar_usuario(usuario, senha)

        elif opcao == "2":
            usuario = input("Usuário: ").strip()
            senha = input("Senha: ")
            autenticar_usuario(usuario, senha)

        elif opcao == "3":
            user = input("Usuário para inspecionar: ").strip()
            exibir_registro_protegido(user)

        elif opcao == "4":
            executar_demonstracao_automatica()
            
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    menu()