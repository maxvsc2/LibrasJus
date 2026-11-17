#cadastro de usario
print("===== LIBRASJUS =====")
print("CADASTRO DE USUÁRIO")

# Solicita o nome completo do usuário.
# Enquanto o campo estiver vazio, o programa pede novamente.

nome = input("Digite seu nome completo: ")
while nome == "":
    print("Nome não informado!")
    nome = input("Digite seu nome novamente: ")

# Solicita o CPF e verifica se possui exatamente 11 caracteres.
# Se não possuir, o usuário deverá digitá-lo novamente.

CPF = input("Digite seu CPF (apenas números): ")
while len(CPF) != 11:     #o len ve o numero de caracteres
    print("O CPF deve conter 11 caracteres!")
    CPF = input("Digite seu CPF novamente: ")

# Solicita a criação de uma senha.
# A senha não pode estar vazia e deve possuir pelo menos 5 caracteres.

senha = input("Crie uma senha: ")
while senha == "" or len(senha) < 5:    
    print("A senha deve conter pelo menos 5 caracteres!")
    senha = input("Digite uma nova senha: ")

# Confirma que o cadastro foi concluído.

print("Cadastro realizado com sucesso!")
print(f"Bem-vindo ao LibrasJus, {nome}!")    #o f puxa a vairavel nome



print("\n===== LOGIN DE USUÁRIO =====")

# Os dados cadastrados anteriormente ficam armazenados
# nas variáveis CPF e senha 

cpf_login = input("Digite seu CPF: ")
senha_login = input("Digite sua senha: ")

# Compara os dados digitados no login com os dados cadastrados.
# O operador != significa "diferente de".
# O operador or permite repetir caso o CPF OU a senha esteja incorreto.

while cpf_login != CPF or senha_login != senha:
    print("CPF ou senha incorretos! Tente novamente.")
    cpf_login = input("Digite seu CPF novamente: ")
    senha_login = input("Digite sua senha novamente: ")

print("Login realizado com sucesso!")
print(f"Bem-vindo de volta ao LibrasJus, {nome}!")
