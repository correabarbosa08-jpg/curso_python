"""
Gerenciador de Senhas
======================
Um gerenciador de senhas simples de linha de comando, com:
- Criptografia forte (AES via Fernet) para o cofre de senhas
- Senha mestra protegida por hash derivado (PBKDF2)
- Comandos para adicionar, listar, buscar, mostrar, remover e gerar senhas
 
Uso:
    python gerenciador_senhas.py
 
Dependências:
    pip install cryptography
"""
 
import os
import sys
import json
import base64
import getpass
import secrets
import string
from pathlib import Path
 
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
 
# ---------------------------------------------------------------------------
# Configurações gerais
# ---------------------------------------------------------------------------
 
ARQUIVO_COFRE = Path.home() / ".gerenciador_senhas" / "cofre.dat"
ARQUIVO_SALT = Path.home() / ".gerenciador_senhas" / "salt.bin"
ITERACOES_PBKDF2 = 480_000  # valor recomendado atualmente (OWASP)
 
 
# ---------------------------------------------------------------------------
# Funções de criptografia
# ---------------------------------------------------------------------------
 
def gerar_ou_carregar_salt() -> bytes:
    """Gera um salt aleatório na primeira execução, ou carrega o existente."""
    ARQUIVO_SALT.parent.mkdir(parents=True, exist_ok=True)
    if ARQUIVO_SALT.exists():
        return ARQUIVO_SALT.read_bytes()
    salt = secrets.token_bytes(16)
    ARQUIVO_SALT.write_bytes(salt)
    return salt
 
 
def derivar_chave(senha_mestra: str, salt: bytes) -> bytes:
    """Deriva uma chave de criptografia a partir da senha mestra usando PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACOES_PBKDF2,
    )
    chave_bruta = kdf.derive(senha_mestra.encode("utf-8"))
    return base64.urlsafe_b64encode(chave_bruta)
 
 
def carregar_cofre(fernet: Fernet) -> dict:
    """Carrega e descriptografa o cofre de senhas. Retorna {} se não existir."""
    if not ARQUIVO_COFRE.exists():
        return {}
    dados_criptografados = ARQUIVO_COFRE.read_bytes()
    try:
        dados_json = fernet.decrypt(dados_criptografados)
    except InvalidToken:
        print("\n❌ Senha mestra incorreta ou arquivo do cofre corrompido.\n")
        sys.exit(1)
    return json.loads(dados_json.decode("utf-8"))
 
 
def salvar_cofre(fernet: Fernet, cofre: dict) -> None:
    """Criptografa e salva o cofre de senhas em disco."""
    ARQUIVO_COFRE.parent.mkdir(parents=True, exist_ok=True)
    dados_json = json.dumps(cofre, indent=2, ensure_ascii=False).encode("utf-8")
    dados_criptografados = fernet.encrypt(dados_json)
    ARQUIVO_COFRE.write_bytes(dados_criptografados)
 
 
# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------
 
def gerar_senha_forte(tamanho: int = 16) -> str:
    """Gera uma senha aleatória forte, com letras, números e símbolos."""
    alfabeto = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        senha = "".join(secrets.choice(alfabeto) for _ in range(tamanho))
        # garante ao menos 1 minúscula, 1 maiúscula, 1 número e 1 símbolo
        if (any(c.islower() for c in senha)
                and any(c.isupper() for c in senha)
                and any(c.isdigit() for c in senha)
                and any(c in "!@#$%^&*()-_=+" for c in senha)):
            return senha
 
 
def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")
 
 
# ---------------------------------------------------------------------------
# Comandos do menu
# ---------------------------------------------------------------------------
 
def cmd_adicionar(cofre: dict) -> None:
    servico = input("Nome do serviço/site (ex.: gmail, netflix): ").strip()
    if not servico:
        print("Nome do serviço não pode ser vazio.")
        return
    usuario = input("Usuário/e-mail: ").strip()
 
    escolha = input("Gerar senha forte automaticamente? (s/n): ").strip().lower()
    if escolha == "s":
        senha = gerar_senha_forte()
        print(f"Senha gerada: {senha}")
    else:
        senha = getpass.getpass("Senha: ")
 
    notas = input("Notas (opcional): ").strip()
 
    cofre[servico] = {
        "usuario": usuario,
        "senha": senha,
        "notas": notas,
    }
    print(f"\n✅ Credenciais para '{servico}' salvas com sucesso.\n")
 
 
def cmd_listar(cofre: dict) -> None:
    if not cofre:
        print("\nO cofre está vazio.\n")
        return
    print("\nServiços cadastrados:")
    for i, servico in enumerate(sorted(cofre.keys()), start=1):
        print(f"  {i}. {servico}")
    print()
 
 
def cmd_mostrar(cofre: dict) -> None:
    servico = input("Nome do serviço a exibir: ").strip()
    entrada = cofre.get(servico)
    if not entrada:
        print(f"\n❌ Nenhuma entrada encontrada para '{servico}'.\n")
        return
    print(f"\n--- {servico} ---")
    print(f"Usuário: {entrada.get('usuario', '')}")
    print(f"Senha:   {entrada.get('senha', '')}")
    if entrada.get("notas"):
        print(f"Notas:   {entrada.get('notas')}")
    print()
 
 
def cmd_remover(cofre: dict) -> None:
    servico = input("Nome do serviço a remover: ").strip()
    if servico in cofre:
        confirmacao = input(f"Confirma remoção de '{servico}'? (s/n): ").strip().lower()
        if confirmacao == "s":
            del cofre[servico]
            print(f"\n🗑️  '{servico}' removido.\n")
    else:
        print(f"\n❌ Nenhuma entrada encontrada para '{servico}'.\n")
 
 
def cmd_gerar_senha() -> None:
    try:
        tamanho = int(input("Tamanho da senha (padrão 16): ") or 16)
    except ValueError:
        tamanho = 16
    print(f"\nSenha gerada: {gerar_senha_forte(tamanho)}\n")
 
 
# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
 
def main() -> None:
    limpar_tela()
    print("=" * 50)
    print("          GERENCIADOR DE SENHAS")
    print("=" * 50)
 
    primeira_vez = not ARQUIVO_SALT.exists()
    if primeira_vez:
        print("\nPrimeiro uso: defina sua senha mestra.")
        print("⚠️  Guarde-a bem — ela NÃO pode ser recuperada se for perdida.\n")
        senha_mestra = getpass.getpass("Crie a senha mestra: ")
        confirmacao = getpass.getpass("Confirme a senha mestra: ")
        if senha_mestra != confirmacao:
            print("\nAs senhas não coincidem. Encerrando.")
            sys.exit(1)
    else:
        senha_mestra = getpass.getpass("\nDigite a senha mestra: ")
 
    salt = gerar_ou_carregar_salt()
    chave = derivar_chave(senha_mestra, salt)
    fernet = Fernet(chave)
 
    cofre = carregar_cofre(fernet)
 
    menu = """
Escolha uma opção:
  1 - Adicionar credencial
  2 - Listar serviços
  3 - Mostrar credencial
  4 - Remover credencial
  5 - Gerar senha forte (sem salvar)
  6 - Salvar e sair
"""
 
    while True:
        print(menu)
        opcao = input("Opção: ").strip()
 
        if opcao == "1":
            cmd_adicionar(cofre)
            salvar_cofre(fernet, cofre)  # salva a cada alteração
        elif opcao == "2":
            cmd_listar(cofre)
        elif opcao == "3":
            cmd_mostrar(cofre)
        elif opcao == "4":
            cmd_remover(cofre)
            salvar_cofre(fernet, cofre)
        elif opcao == "5":
            cmd_gerar_senha()
        elif opcao == "6":
            salvar_cofre(fernet, cofre)
            print("\n💾 Cofre salvo. Até logo!\n")
            break
        else:
            print("\nOpção inválida.\n")
 
 
if __name__ == "__main__":
    main()
 