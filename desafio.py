import textwrap

def menu():
    menu = '''\n
                   Bem-vindo ao Banco Python!

                  =========== MENU ===========

                  [d]\t Depositar
                  [s]\t Sacar
                  [e]\t Extrato
                  [nc]\t Nova Conta
                  [lc]\t Listar Contas
                  [nu]\t Novo Usuário
                  [q]\t Sair

                  ============================
    ''' 
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        print(f"Depósito de: R$ {valor:.2f} realizado com sucesso!")
        extrato += f'''
        Depósito de: R$ {valor:.2f}'''

    else:
        print("Operação Cancelada! O valor Informado não é válido.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação Cancelada! Você não possui saldo suficiente.")

    elif excedeu_limite:
        print("Operação Cancelada! O valor do saque excedeu o limite.")

    elif excedeu_saques:
        print("Operação Cancelada! Número máximo de saques foi excedido.")

    elif valor > 0:
        saldo -= valor
        print(f"Saque de: R$ {valor:.2f} realizado com sucesso!")
        extrato += f'''
        Saque de: R$ {valor:.2f}'''
        numero_saques += 1

    else:
        print("Operação Cancelada! O valor informado não é válido.")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print('''
                ========= Extrato ==========
                ''')
    print('''
                não foram realizadas movimentações.
                ''' if not extrato else extrato)
    print(f'''
                Saldo: R$ {saldo:.2f}
                ''')
    print('''
                ============================
                ''')

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("Usuário não encontrado, Criação de conta encerrada!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            print('''
                ========= Depósito =========
                ''')
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            print('''
                ========== Saque ===========
                ''')
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar o Banco Python, tenha um bom dia!")
            break

        else:
            print("Operação Inválida! Por favor selecione um item do MENU.")

main()