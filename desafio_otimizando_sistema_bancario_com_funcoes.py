import textwrap
from datetime import datetime

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /): 
    if valor > 0:
        print("Coloque o dinheiro no caixa!\n")
        saldo += valor
        data_agora = datetime.now()
        hora_convertida = data_agora.strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"Depósito de R${valor:.2f} às {hora_convertida}\n"
    else:
        print("Valor informado inválido!\n")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saque = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saque: #Função saque deve receber argumentos apenas por nome (keyword only). Sugestões: Saldo, valor, extrato, limite, numero_saques, limite_saques. Retorno: Saldo e extrato
        print("Sua conta não possui saldo suficiente para essa ação!\n")
    elif excedeu_limite:
        print("Sua conta não permite sacar valores acima de 500 reais!\n")
    elif excedeu_saques:
        print("Limite de saques diário atingido!\n")
    elif valor > 0:
        numero_saques += 1
        saldo -= valor
        data_agora = datetime.now()
        hora_convertida = data_agora.strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"Saque de R${valor:.2f} realizado às {hora_convertida}\n"
        print("Retire seu dinheiro!\n")
    else:
        print("Valor Inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n============Extrato============")
    print("Não foram realizadas movimentações bancárias hoje.\n" if not extrato else extrato)
    print(f"\n Saldo:R${saldo:.2f}")
    print("\n===============================")

def criar_usuarios(usuarios): 
    cpf = input("\nInforme seu cpf (apenas números): ")
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        print("\nUsuário já cadastrato!")
        return
    else:
        nome = input("\nInforme seu nome:")
        data_nascimento = input("\nInforme sua data de nascimento (dd-mm-aaaa):")
        endereco = input("\nInforme seu endereço (logradouro-nro, bairro, cidade/estado):")
        usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
        print("\nUsuário Cadastrado!")

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe seu CPF:")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("Sua conta acabou de ser criada")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nUsuário não encontrado. Favor verificar cpf ou cadastrar novo usuario")

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

    saldo = 20
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            
        elif opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuarios(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
