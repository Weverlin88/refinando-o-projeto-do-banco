import textwrap

def menu():
    menu = """\n
    Bem-vindo ao Vevi's Bank. Escolha uma das seguintes operações:
    ========== MENU ==========
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tExcluir conta
    [8]\tSair 
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nXXX Operação falhou! O valor informado é inválido. XXX")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > LIMITE_SAQUES

    if excedeu_saldo:
        print('\nxxx Saldo insuficiente xxx')

    elif excedeu_limite:
        print('\nxxx O valor do saque excede o limite permitido xxx')

    elif excedeu_saques:
        print('\nxxx Número de saques excedido xxx')

    elif valor > 0:
        saldo -= valor
        extrato += f'Saque\t\tR$ {valor:.2f}\n'
        numero_saques =+ 1
        print('\n=== Saque realizado com sucesso! ===')

    else:
        print('\nXXX Operação falhou! O valor informado é inválido. XXX')

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n====== Extrato ======")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("=========================")


def criar_usuario(usuarios):
    nome = input('Digite seu nome completo: ')
    cpf = input("Informe seu CPF (somente números): ")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa):")
    endereco = input("Informe seu endereço (rua, nº, bairro, cidade/estado):")
    email = input('Digite seu e-mail para contato: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nXXX Já existe um usuário com esse CPF! XXX")
    
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereço": endereco, "email": email})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios, saldo):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0}
        return conta
    print("\nXXX Usuário não encontrado, criação de conta encerrada. XXX")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print (linha + "\n======================" )
        print(textwrap.dedent(linha))

def excluir_conta(contas):
    numero_conta = int(input("Informe o número da conta que deseja excluir: "))
    conta_encontrada = None

    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada:
         if "saldo" in conta_encontrada and conta_encontrada["saldo"] == 0:
            contas.remove(conta_encontrada)
            print("\n=== Conta excluída com sucesso! ===")
         else:
            print("\nXXX A conta possui saldo diferente de zero. Não é possível excluí-la. XXX")
    else:
        print("\nXXX Conta não encontrada. XXX")

def main():
    global LIMITE_SAQUES
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    limite = 500
    saldo = 0
    extrato = ""
    numero_saques = 0 
    usuarios = []
    contas = []
    numero_conta = 1
    
    while True:
        opcao = menu()

        if opcao == '1':
            valor = float(input("Informe o valor de depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == '2':
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == '4':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios, saldo=0)  # Adicionando o argumento "saldo=0"
            
            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '6':
            criar_usuario(usuarios)

        elif opcao == '7':
            excluir_conta(contas)

        elif opcao == '8':
            break

        else:
            print("Operação inválida. Por favor selecione novamente a opção desejada")

if __name__ == "__main__":
    main()
