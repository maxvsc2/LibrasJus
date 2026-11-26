
import json
import os
import hashlib

ARQUIVO = "usuarios.json"
ARQUIVO_ATENDIMENTOS = "atendimentos.json"

# Tupla: assuntos disponíveis para os atendimentos
ASSUNTOS = ("Processo", "Audiência", "Orientação jurídica")


# ==========================================
# CRIPTOGRAFAR SENHA
# ==========================================

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# ==========================================
# CARREGAR USUARIOS
# ==========================================

def carregar_usuarios():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("Formato inválido de usuários")
            return dados
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError, ValueError) as erro:
        print(f"Erro ao carregar usuários: {erro}")
        return None


# ==========================================
# SALVAR USUARIOS
# ==========================================

def salvar_usuarios(usuarios):
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
        return True
    except OSError as erro:
        print(f"Erro ao salvar usuários: {erro}")
        return False


# ==========================================
# CARREGAR ATENDIMENTOS
# ==========================================

def carregar_atendimentos():
    try:
        with open(ARQUIVO_ATENDIMENTOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("Formato inválido de atendimentos")
            return dados
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError, ValueError) as erro:
        print(f"Erro ao carregar atendimentos: {erro}")
        return None


# ==========================================
# SALVAR ATENDIMENTOS
# ==========================================

def salvar_atendimentos(atendimentos):
    try:
        with open(ARQUIVO_ATENDIMENTOS, "w", encoding="utf-8") as arquivo:
            json.dump(atendimentos, arquivo, indent=4, ensure_ascii=False)
        return True
    except OSError as erro:
        print(f"Erro ao salvar atendimentos: {erro}")
        return False


# ==========================================
# CADASTRO
# ==========================================

def cadastro():

    print("\n===== CRIAR CONTA =====")

    usuarios = carregar_usuarios()
    if usuarios is None:
        return

    nome = input("Nome completo: ").strip()
    cpf = input("CPF: ").strip()

    for usuario in usuarios:

        if usuario["cpf"] == cpf:

            print("CPF já cadastrado!")
            return

    email = input("E-mail: ").strip()
    senha = input("Crie uma senha: ")
    if not nome or not email or not senha:
        print("Nome, e-mail e senha são obrigatórios!")
        return
    if not cpf.isdigit() or len(cpf) != 11:
        print("O CPF deve conter 11 números!")
        return
    if len(senha) < 5:
        print("A senha deve ter pelo menos 5 caracteres!")
        return

    novo_usuario = {

        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": criptografar_senha(senha)

    }

    usuarios.append(novo_usuario)

    if salvar_usuarios(usuarios):
        print("\nCadastro realizado com sucesso!")


# ==========================================
# LOGIN
# ==========================================

def login():

    print("\n===== ENTRAR =====")

    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua senha: ")

    usuarios = carregar_usuarios()
    if usuarios is None:
        return None

    for usuario in usuarios:

        if (usuario.get("cpf") == cpf and
            usuario.get("senha") == criptografar_senha(senha)):

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
    if usuarios is None:
        return

    for usuario in usuarios:

        if usuario.get("cpf") == cpf:

            print("\nRecuperação de senha indisponível nesta versão demonstrativa.")
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
        print("4 - Meu perfil (consultar, editar ou excluir)")
        print("5 - Sair da conta")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            atendimento(usuario)

        elif opcao == "2":

            acompanhar_atendimentos(usuario)

        elif opcao == "3":

            print("\nBem-vindo ao LibrasJus!")
            print("Sistema de apoio à comunicação em Libras.")

        elif opcao == "4":

            if not gerenciar_perfil(usuario):
                break

        elif opcao == "5":

            print("Saindo da conta...")
            break

        else:

            print("Opção inválida!")


# ==========================================
# PERFIL DO USUÁRIO: CONSULTAR, EDITAR, EXCLUIR
# ==========================================

def gerenciar_perfil(usuario):
    """Retorna False quando a conta é excluída (logout automático)."""
    while True:
        print("\n===== MEU PERFIL =====")
        print("1 - Consultar meus dados")
        print("2 - Atualizar nome e e-mail")
        print("3 - Excluir minha conta")
        print("4 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Nome:", usuario["nome"])
            print("CPF:", usuario["cpf"])
            print("E-mail:", usuario["email"])
        elif opcao == "2":
            novo_nome = input("Novo nome (Enter mantém o atual): ").strip()
            novo_email = input("Novo e-mail (Enter mantém o atual): ").strip()
            usuarios = carregar_usuarios()
            if usuarios is None:
                continue
            for item in usuarios:
                if item.get("cpf") == usuario["cpf"]:
                    item["nome"] = novo_nome or item["nome"]
                    item["email"] = novo_email or item["email"]
                    if salvar_usuarios(usuarios):
                        usuario.update(item)
                        print("Perfil atualizado!")
                    break
        elif opcao == "3":
            confirmacao = input("Digite EXCLUIR para confirmar: ")
            if confirmacao != "EXCLUIR":
                print("Exclusão cancelada.")
                continue
            usuarios = carregar_usuarios()
            atendimentos = carregar_atendimentos()
            if usuarios is None or atendimentos is None:
                continue
            # Primeiro apaga os atendimentos vinculados ao CPF.
            restantes = [item for item in atendimentos if item.get("cpf") != usuario["cpf"]]
            if not salvar_atendimentos(restantes):
                continue
            restantes_usuarios = [item for item in usuarios if item.get("cpf") != usuario["cpf"]]
            if salvar_usuarios(restantes_usuarios):
                print("Conta excluída. Você saiu do sistema.")
                return False
            print("Não foi possível concluir a exclusão da conta.")
        elif opcao == "4":
            return True
        else:
            print("Opção inválida!")


# ==========================================
# ATENDIMENTO
# ==========================================

def atendimento(usuario):

    print("\n===== ATENDIMENTO =====")
    print("Assuntos disponíveis:")
    for indice, assunto in enumerate(ASSUNTOS, start=1):
        print(f"{indice} - {assunto}")
    escolha = input("Escolha o assunto: ")
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(ASSUNTOS):
        print("Assunto inválido!")
        return
    assunto_escolhido = ASSUNTOS[int(escolha) - 1]
    print("Conectando com intérprete em Libras... (simulação em texto)")

    iniciar = input("Deseja iniciar o atendimento? (s/n): ")

    if iniciar.lower() == "s":

        historico = []

        # Iniciar conversa
        conversa(historico)

        # SALVAR ATENDIMENTO AUTOMATICAMENTE
        if len(historico) > 0:

            salvar_novo_atendimento(usuario, historico, assunto_escolhido)

            print("\nAtendimento registrado!")

            # Confirmação dos dados
            print("\n===== CONFIRMAÇÃO =====")
            print("Tipo: Atendimento")
            print("Assunto:", assunto_escolhido)
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

def salvar_novo_atendimento(usuario, historico, assunto="Processo"):

    atendimentos = carregar_atendimentos()
    if atendimentos is None:
        return

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
        "assunto": assunto,
        "unidade": "Vara Cível",
        "historico": historico

    }

    # Adicionar à lista
    atendimentos.append(novo_atendimento)

    # Gravar no arquivo
    if not salvar_atendimentos(atendimentos):
        return

    print("\nAtendimento salvo com sucesso!")

    print("Arquivo localizado em:")
    print(os.path.abspath(ARQUIVO_ATENDIMENTOS))


# ==========================================
# ACOMPANHAR ATENDIMENTOS
# ==========================================

def acompanhar_atendimentos(usuario):

    atendimentos = carregar_atendimentos()
    if atendimentos is None:
        return

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

if __name__ == "__main__":
    acesso()
