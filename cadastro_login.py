import hashlib
import os


import json

import hmac

with open("usuarios.json", "r", encoding="utf-8") as arquivo:
    usuarios = json.load(arquivo)
print(usuarios)



#cadastro de usario

print("1- Cadastrar usuário")
print("2- Login")
print("3- Sair")

opcao = input("Digite a opção escolhida: ")

if opcao == "1":
    print("CADASTRO DE USUÁRIO")

    nome = input("Digite seu nome completo: ")    
    while nome == "":
        print("Nome não informado!")
        nome = input("Digite seu nome novamente: ")

    CPF = input("Digite seu CPF: ")
    while len(CPF) != 11:    
        print("CPF inválido!")
        CPF = input("Digite seu CPF novamente: ")

    senha = input("Crie uma senha: ")
    while senha == "" or len(senha) < 5:
        print("A senha deve conter pelo menos 5 caracteres!")
        senha = input("Digite uma nova senha: ")
    salt = os.urandom(16)

    hash_senha = hashlib.scrypt(
         senha.encode("utf-8"),
        salt=salt,
        n=16384,
         r=8,
         p=1
     )

    usuario = {
      "nome": nome,
      "cpf": CPF,
      "salt": salt.hex(),
      "hash_senha": hash_senha.hex()
    }
    usuarios.append(usuario)
    print(usuario["nome"])
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
      json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    print(usuarios)

    print("Cadastro realizado com sucesso!")
    print(f"Bem-vindo ao LibrasJus, {nome}!")    #o f puxa a vairavel nome


elif opcao == "2":
    print("LOGIN DE USUÁRIO") 

    cpf_login = input("Digite seu CPF: ")
    senha_login = input("Digite sua senha: ")

    cpf_encontrado = False
    for usuario in usuarios:
      if cpf_login == usuario["cpf"]:
        cpf_encontrado = True
        salt_salvo = bytes.fromhex(usuario["salt"])
        hash_login = hashlib.scrypt(
           senha_login.encode("utf-8"),
    salt=salt_salvo,
     n=16384,
    r=8,
    p=1
)
        hash_salvo = bytes.fromhex(usuario["hash_senha"])
        if hmac.compare_digest(hash_login, hash_salvo):
         print("Login realizado com sucesso!")
        else:
            print("CPF ou senha incorretos!")

        if cpf_encontrado == False:
         print("Conta não encontrada!")
        
elif opcao == "3": 
    print("Encerrando")

else: 
    print("opcao invalida!")

