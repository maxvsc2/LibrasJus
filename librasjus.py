
import json
import os
import hashlib

ARQUIVO = "usuarios.json"
ARQUIVO_ATENDIMENTOS = "atendimentos.json"


# ==========================================
# CRIPTOGRAFAR SENHA
# ==========================================

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# ==========================================
# CARREGAR USUARIOS
# ==========================================

def carregar_usuarios():

    if os.path.exists(ARQUIVO):

        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return []


# ==========================================
# SALVAR USUARIOS
# ==========================================

def salvar_usuarios(usuarios):

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)


# ==========================================
# CARREGAR ATENDIMENTOS
# ==========================================

def carregar_atendimentos():

    if os.path.exists(ARQUIVO_ATENDIMENTOS):

        with open(ARQUIVO_ATENDIMENTOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return []


# ==========================================
# SALVAR ATENDIMENTOS
# ==========================================

def salvar_atendimentos(atendimentos):

    with open(ARQUIVO_ATENDIMENTOS, "w", encoding="utf-8") as arquivo:
        json.dump(atendimentos, arquivo, indent=4, ensure_ascii=False)


# ==========================================
# CADASTRO
# ==========================================

def cadastro():

    print("\n===== CRIAR CONTA =====")

    usuarios = carregar_usuarios()

    nome = input("Nome completo: ")
    cpf = input("CPF: ")

    for usuario in usuarios:

        if usuario["cpf"] == cpf:

            print("CPF já cadastrado!")
            return

    email = input("E-mail: ")
    senha = input("Crie uma senha: ")

    novo_usuario = {

        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": criptografar_senha(senha)

    }

    usuarios.append(novo_usuario)

    salvar_usuarios(usuarios)

    print("\nCadastro realizado com sucesso!")


# ==========================================
# LOGIN
# ==========================================

def login():

    print("\n===== ENTRAR =====")

    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")

    usuarios = carregar_usuarios()

    for usuario in usuarios:

        if (usuario["cpf"] == cpf and
            usuario["senha"] == criptografar_senha(senha)):

            print("\nBem-vindo(a),", usuario["nome"])

            return usuario

    print("\nCPF ou senha incorretos!")

    return None


# ==========================================
# RECUPERAR SENHA
# ==========================================

def recuperar_senha():

    print("\n===== ESQUECI MINHA SENHA =====")

    cpf = input("Digite seu CPF: ")

    usuarios = carregar_usuarios()

    for usuario in usuarios:

        if usuario["cpf"] == cpf:

            print("\nSenha enviada para o seu email")
            return

    print("\nCPF não encontrado!")


# ==========================================
# TELA DE ACESSO
# ==========================================

def acesso():

    while True:

        print("\n===== LIBRASJUS =====")
        print("1 - Entrar com CPF")
        print("2 - Criar conta")
        print("3 - Esqueci minha senha")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            usuario = login()

            if usuario:
                menu_inicial(usuario)

        elif opcao == "2":

            cadastro()

        elif opcao == "3":

            recuperar_senha()

        elif opcao == "4":

            print("Encerrando o LibrasJus...")
            break

        else:

            print("Opção inválida!")


# ==========================================
# MENU INICIAL
# ==========================================

def menu_inicial(usuario):

    while True:

        print("\n===== MENU INICIAL =====")
        print("1 - Atendimento em Libras")
        print("2 - Acompanhar meus atendimentos")
        print("3 - Informações")
        print("4 - Sair da conta")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            atendimento(usuario)

        elif opcao == "2":

            acompanhar_atendimentos(usuario)

        elif opcao == "3":

            print("\nBem-vindo ao LibrasJus!")
            print("Sistema de apoio à comunicação em Libras.")

        elif opcao == "4":

            print("Saindo da conta...")
            break

        else:

            print("Opção inválida!")


# ==========================================
# ATENDIMENTO
# ==========================================

def atendimento(usuario):

    print("\n===== ATENDIMENTO =====")
    print("Conectando com intérprete em Libras...")

    iniciar = input("Deseja iniciar o atendimento? (s/n): ")

    if iniciar.lower() == "s":

        historico = []

        # Iniciar conversa
        conversa(historico)

        # SALVAR ATENDIMENTO AUTOMATICAMENTE
        if len(historico) > 0:

            salvar_novo_atendimento(usuario, historico)

            print("\nAtendimento registrado!")

            # Confirmação dos dados
            print("\n===== CONFIRMAÇÃO =====")
            print("Tipo: Atendimento")
            print("Assunto: Processo")
            print("Unidade: Vara Cível")

            opcao = input("Os dados estão corretos? (s/n): ")

            if opcao.lower() == "s":

                conclusao()

            else:

                print("Atendimento registrado, mas não confirmado.")

        else:

            print("\nNenhuma mensagem foi registrada.")
            print("Atendimento não salvo.")

    else:

        print("Atendimento cancelado.")


# ==========================================
# CONVERSA
# ==========================================

def conversa(historico):

    print("\n===== CONVERSA =====")
    print("Digite suas mensagens.")
    print("Digite 'fim' para encerrar.")

    while True:

        mensagem = input("\nUsuário: ")

        if mensagem.lower() == "fim":
            break

        historico.append({

            "remetente": "Usuário",
            "mensagem": mensagem

        })

        resposta = input("Conciliador: ")

        if resposta.lower() == "fim":
            break

        historico.append({

            "remetente": "Conciliador",
            "mensagem": resposta

        })


# ==========================================
# SALVAR NOVO ATENDIMENTO
# ==========================================

def salvar_novo_atendimento(usuario, historico):

    atendimentos = carregar_atendimentos()

    # Contar atendimentos do usuário
    numero = 1

    for item in atendimentos:

        if item["cpf"] == usuario["cpf"]:

            numero += 1

    # Criar novo atendimento
    novo_atendimento = {

        "cpf": usuario["cpf"],
        "numero": numero,
        "titulo": f"Atendimento {numero:02d}",
        "tipo": "Atendimento",
        "assunto": "Processo",
        "unidade": "Vara Cível",
        "historico": historico

    }

    # Adicionar à lista
    atendimentos.append(novo_atendimento)

    # Gravar no arquivo
    salvar_atendimentos(atendimentos)

    print("\nAtendimento salvo com sucesso!")

    print("Arquivo localizado em:")
    print(os.path.abspath(ARQUIVO_ATENDIMENTOS))


# ==========================================
# ACOMPANHAR ATENDIMENTOS
# ==========================================

def acompanhar_atendimentos(usuario):

    atendimentos = carregar_atendimentos()

    # Filtrar atendimentos do usuário logado
    meus_atendimentos = []

    for item in atendimentos:

        if item["cpf"] == usuario["cpf"]:

            meus_atendimentos.append(item)

    # Verificar se existem atendimentos
    if not meus_atendimentos:

        print("\nNenhum atendimento encontrado.")
        return

    # Menu de atendimentos
    while True:

        print("\n===== MEUS ATENDIMENTOS =====")

        for i, item in enumerate(meus_atendimentos, start=1):

            print(f"{i} - {item['titulo']}")

        print("0 - Voltar ao menu inicial")

        opcao = input("\nEscolha um atendimento: ")

        if opcao == "0":

            break

        elif opcao.isdigit():

            numero = int(opcao)

            if 1 <= numero <= len(meus_atendimentos):

                atendimento_selecionado = meus_atendimentos[numero - 1]

                mostrar_historico(atendimento_selecionado)

            else:

                print("Atendimento não encontrado!")

        else:

            print("Opção inválida!")


# ==========================================
# MOSTRAR HISTORICO
# ==========================================

def mostrar_historico(atendimento):

    print("\n===== HISTÓRICO DO ATENDIMENTO =====")

    print("Atendimento:", atendimento["titulo"])
    print("Tipo:", atendimento["tipo"])
    print("Assunto:", atendimento["assunto"])
    print("Unidade:", atendimento["unidade"])

    print("\n===== CONVERSA =====")

    for mensagem in atendimento["historico"]:

        print(f"\n{mensagem['remetente']}:")
        print(mensagem["mensagem"])

    print("\n===== FIM DO HISTÓRICO =====")


# ==========================================
# CONCLUSÃO
# ==========================================

def conclusao():

    print("\n===== ACORDO CONCLUÍDO =====")
    print("Atendimento concluído com sucesso!")

    opcao = input("Deseja ver os detalhes? (s/n): ")

    if opcao.lower() == "s":

        print("Tipo: Atendimento")
        print("Assunto: Processo")
        print("Unidade: Vara Cível")


# ==========================================
# EXECUTAR SISTEMA
# ==========================================

acesso()
