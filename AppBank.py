import pickle
import sys
import os



if os.path.getsize('data.pickle') > 0:
    with open('data.pickle', 'rb') as p:
        unpickler = pickle.Unpickler(p)
        data = unpickler.load()
else:
    data = dict()

Contas = dict(cod=[], saldo=[], tr=[])
cliente = dict(cod=[], nome=[], cidade=[], telefone=[], cc=[])
Trans = dict(cod=[], tipo=[], origem=[], destino=[], valor=[])

if data.get('Contas'):
    Contas = data.get('Contas')
if data.get('cliente'):
    cliente = data.get('cliente')
if data.get('Trans'):
    Trans = data.get('Trans')

def sair():
    data = dict(Contas=Contas, cliente=cliente, Trans=Trans)
    with open('data.pickle', 'wb') as p:
        pickle.dump(data, p)
    sys.exit()


def novoCliente():
    print('------- 1 - CADASTRO CLIENTE / C.C ---------------\n')
    qtdecliente = len(cliente['cod'])+1
    cod = qtdecliente
    nome = input('NOME: ')
    nome.upper()
    telefone = input('TELEFONE: ')
    cidade = input('CIDADE: ')
    cidade.upper()
    cc = cod
    depinicial = input('DEPÓSITO INICIAL: ')
    depinicial = float(depinicial)
    cliente['cod'].append(cod)
    cliente['nome'].append(nome)
    cliente['cidade'].append(cidade)
    cliente['telefone'].append(telefone)
    Contas['cod'].append(cc)
    Contas['saldo'].append(depinicial)
    print('Cliente Cadastrado com Sucesso!!!\n')
    print('Nome do Cliente: {} \nSeu Codigo é: {} \nConta-Corrente Numero: {} Criado com Sucesso!!!! \nDepósito inicial de R$: {}'.format(nome, cod, cc, depinicial))
    monta_menu(menu_principal)


def consultaCliente():
    print('--------------- 2. CONSULTA CLIENTE ---------------\n')
    consultar = input("Qual o codigo do cliente?: ")
    consultarV = consultar in cliente['cod']
    if consultarV:
        pos = cliente['cod'].index(consultar)
        print('Cliente Localizado Com sucesso!\n')
        print('')
        print("Codigo \t Nome \t Cidade \t Telefone \t Saldo Atual")
        print("  {0}    \t {1} \t {2} \t {3} \t {4} \n".format(cliente['cod'][pos], cliente['nome'][pos], cliente['cidade'][pos],
                                                cliente['telefone'][pos], Contas['saldo'][pos]))
        monta_menu(menu_principal)
    else:
        print('Cliente Não Localizado, tente novamente\n')
        monta_menu(menu_cadastro)


def listaCliente():
    print('------3. LISTA DE CLIENTES -----\n')
    print("CODIGO  -  NOME          -          TELEFONE")
    if len(cliente['cod']) < 1:
        print('\nNão Existe Cliente Cadastrado\n')
        monta_menu(menu_cadastro)
    else:
        i=0
        while i < len(cliente):
            print(f"{cliente['cod'][i]}\t\t   {cliente['nome'][i]} \t\t\t\t{cliente['telefone'][i]}\n\n")
            monta_menu(menu_principal)


def transDeposito() -> object:
    print('---------- 3.1 REALIZANDO DEPÓSITO -----------')
    consultar = input("\nInforme o codigo da conta em que deseja realizar o deposito: \n")
    consultarV = consultar in Contas['cod']
    if consultarV:
        pos = Contas['cod'].index(consultar)
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format(cliente['nome'][pos], Contas['saldo'][pos]))  #Buquei cliente no banco de dados e imprimi
        deposito = float(input("\nInforme o valor do deposito: "))
        deposito = float(deposito)
        valor = Contas['saldo'][pos]
        valor = valor + deposito
        Contas['saldo'][pos] = valor
        print('Deposito realizado com Sucesso!!!\n')
        print('Olá {} tudo bem?, \nSaldo atual da Conta é de R$: {}'.format(cliente['nome'][pos],
                                                                                           Contas['saldo'][pos]))
        monta_menu(menu_principal)
    else:
        print("Conta nao existe!!")
        monta_menu(menu_principal)


def transSaque() -> object:
    print('---------- 3.1 REALIZANDO SAQUE -----------')
    consultar = input("\nInforme o Numero da Conta-Corrente que deseja realizar o SAQUE: ")
    consultarV = consultar in Contas['cod']
    if consultarV:
        pos = Contas['cod'].index(consultar)
        print()
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format (cliente['nome'][pos],
                                                                                        Contas['saldo'][pos]))
        saque = input("\nValor do saque R$:_ ")
        saque = float(saque)
        valor = Contas['saldo'][pos]
        if saque <= valor:
            valor -= saque
            Contas['saldo'][pos] = valor
            print('Olá {} tudo bem?, o Saldo atual da sua Conta-Corrente é de R$: {}'.format(cliente['nome'][pos],
                                                                                            Contas['saldo'][pos]))
            monta_menu(menu_principal)
        else:
            print('{} voce não tem saldo para realizar saque de R$ {}'.format(cliente['nome'][pos], saque))
            monta_menu(menu_trans)


def transFerencia():
    print('---------- TRANSFERENCIA -----------')
    transcontasaque = input("\nInforme o Numero da Conta-Corrente que deseja SACAR: ")
    if transcontasaque in Contas['cod']:
        pos1 = Contas['cod'].index(transcontasaque)
        print('Bem Vindo {} o seu SALDO é de R$ {}'.format(cliente['nome'][pos1], Contas['saldo'][pos1]))
        transferevalor = input('Informe o valor da TRANSFERÊNCIA R$ ')
        transferevalor = float(transferevalor)
        if transferevalor > Contas['saldo'][pos1]:
            print('Voce não tem saldo para realizar a transferência de R$'.format(Contas['saldo'][pos1]))
            monta_menu(menu_principal)
        else:
            transfcontadeposito = input('Informe o Numero da Conta-Corrente que deseja DEPOSITAR: ')
            if transfcontadeposito in Contas['cod']:
                pos2 = Contas['cod'].index(transfcontadeposito)
                print('---------Transferencia Efetuada com Sucesso!!!---------')
                print('O titular da Conta-Corrente é {}'.format(cliente['nome'][pos2]))
                Contas['saldo'][pos1] = Contas['saldo'][pos1] - transferevalor
                Contas['saldo'][pos2] = Contas['saldo'][pos2] + transferevalor
                print('{} o saldo atual da sua Conta-Corrente é R$ {}'.format(cliente['nome'][pos1], Contas['saldo'][pos1]))
                monta_menu(menu_principal)
            else:
                print('Conta Corrente não Localizada')
                monta_menu(menu_principal)
    else:
        print('Conta Corrente Não Localizada')
        monta_menu(menu_principal)


menu_cadastro = {
    '1': ('- Cadastro', novoCliente),
    '2': ('- Consulta', consultaCliente),
    '3': ('- Lista', listaCliente),
    '9': ('- Deslogar', sair),
}
menu_trans = {
    '1': ('- Depósito', transDeposito),
    '2': ('- Saque', transSaque),
    '3': ('- Transferência', transFerencia),
    '9': ('- Voltar', menu_cadastro),
}
menu_principal = {
    '1': ('- Clientes', menu_cadastro),
    '2': ('- Transações', menu_trans),
    '9': ('- Deslogar', sair),
}
def monta_menu(menu) -> object:
    print()
    print('******* Sistema VBANK *******:')
    print('')
    for k, v in menu.items():
        texto, _ = v
        print(k, texto)
    print('')
    opcao = input('Digite a Opçao Desejada:    ')
    print('')
    try:
        escolhido = menu[opcao]
        _, funcao = escolhido
        if isinstance(funcao, dict):
            monta_menu(funcao)
        else:
            funcao()
    except KeyError:
        print('')
        monta_menu(menu_principal)


if __name__ == '__main__':
    monta_menu(menu_principal)
