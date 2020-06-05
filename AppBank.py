import pickle
import sys
import os
import requests


if os.path.getsize('data.pickle') > 0:
    with open('data.pickle','rb') as p:
        unpickler = pickle.Unpickler(p)
        data = unpickler.load()
else:
    data = dict()

Contas = dict(cod=[], saldo=[], tr=[])
cliente = dict(cod=[], nome=[], cidade=[], telefone=[], cc=[], address_data=[])
Trans = dict(cod=[], tipo=[], origem=[], destino=[], valor=[])
numClientes = 0


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

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def startsystem():
    global numClientes
    cls()
    menuInicial = '''
********* MENU INICIAL ***********  

*    1 - CADASTRO DE CLIENTE     *
*    2 - REALIZAR TRANSAÇÃO      *
*    9 - SAIR                    *
'''
    print(menuInicial)
    print('*    Existem {} Clientes Castrados'.format(len(cliente['cod'])))

    startSystemm = '1', '2', '9'
    while startSystemm:
        starSystemm = input('*    DIGITE A OPÇÃO DESEJADA:__  ')
        print('Digite somente as Opções do Menu: ')
        cls()
        if starSystemm == '1':
            menuCliente()
        elif starSystemm == '2':
            menuTrans()
        elif starSystemm == '9':
            sair()
        else:
            print('OPÇÃO INVÁLIDA!')
            startsystem()

def menuCliente():
    cls()
    menuCli = '''
********* MENU CLIENTE ***********

*    1 - CADASTRO
*    2 - CONSULTA
*    3 - LISTAR DE CLIENTES
*    9 - VOLTAR 
'''
    print(menuCli)
    menuCli = '1', '2', '3', '9'
    while menuCli:
        menuCli = input('*    DIGITE A OPÇÃO DESEJADA:__   ')
        print('Digite somente as Opções do Menu: ')
        cls()
        print()
        if menuCli == '1':
            novoCliente()
        if menuCli == '2':
            consultaCliente()
        if menuCli == '3':
            listaCliente()
        if menuCli == '9':
            startsystem()

def menuTrans():
    cls()
    menupTrans = '''
********* MENU TRANSAÇÕES ***********
* 1 - DEPOSITO
* 2 - SAQUE
* 3 - TRANSFERENCIA - (em manutenção)
* 4 - IMPRIMIR LISTA TRANSAÇÕES - (em manutenção)
* 5 - VOLTAR 
'''
    print(menupTrans)
    opcoesmtrans = '1', '2', '3', '4', '5'
    while opcoesmtrans:
        opcoesmtrans = input('* DIGITE A OPÇÃO DESEJADA:__   ')
        cls()
        if opcoesmtrans == '1':
            transDeposito()
        if opcoesmtrans == '2':
            transSaque()
        if opcoesmtrans == '3':
            transFerencia()
        if opcoesmtrans == '4':
            transLista()
        if opcoesmtrans == '5':
            startsystem()
        print('Digite somente as Opções do Menu: ')

def consultaCep():  # <------ Consulta API Correios para busca de CEP
    menuCep = ''' ---------------------------
----- Consulta CEP --------
--------------------------- '''
    print(menuCep)
    cep_input = input('Digite o CEP para a consulta: ')

    if len(cep_input) != 8:
        option1 = int(input('CEP Inválido, Deseja realizar uma nova consulta ?\n1. Sim\n2. Sair\n'))
        if option1 == 1:
            startsystem()
        else:
            print('Saindo...')
            exit()

    request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep_input))

    address_data = request.json()

    if 'erro' not in address_data:
        print('==> CEP ENCONTRADO <==')

        print('CEP: {}'.format(address_data['cep']))
        print('Logradouro: {}'.format(address_data['logradouro']))
        print('Complemento: {}'.format(address_data['complemento']))
        print('Bairro: {}'.format(address_data['bairro']))
        print('Cidade: {}'.format(address_data['localidade']))
        print('Estado: {}'.format(address_data['uf']))
    else:
        print('{}: CEP inválido.'.format(cep_input))

    print('---------------------------------')
    option = int(input('Deseja realizar uma nova consulta ?\n1. Sim\n2. Sair\n'))
    if option == 1:
        startsystem()
    else:
        print('Saindo...')


def novoCliente():
    cls()
    print('------- 1 - CADASTRO CLIENTE / C.C ---------------')
    print()
    cod = input('CODIGO DO CLIENTE: ')
    nome = input('NOME: ')
    telefone = input('TELEFONE: ')
    cidade = input('CIDADE: ')
    cc = input('N. CONTA-CORRENTE: ')
    depinicial = input('DEPÓSITO INICIAL: ')
    depinicial = float(depinicial)
    print('')
    cliente['cod'].append(cod)
    cliente['nome'].append(nome)
    cliente['cidade'].append(cidade)
    cliente['telefone'].append(telefone)
    Contas['cod'].append(cc)
    Contas['saldo'].append(depinicial)

    print('Cliente: {}, seu Codigo é: {}, Conta-Corrente Numero: {} foi criado com Sucesso!!!!, depósito inicial de: {}'.format(nome, cod, cc, depinicial))
    print('')
    contador()

    listavolta = 0
    while listavolta != '9':
        listavolta = input('DIGITE 9 MENU INICIAL: ')
        print('Digite somente as Opções do Menu: ')
        print('Opção Inválida')
    else:
        startsystem()
        cls()
    print('')


def consultaCliente():  # ----------- ("NOVO")Função Consultar novo Cliente ---------------
    cls()
    print('------------------------- 2. CONSULTA CLIENTE ----------------------')
    consultar = input("\nQual o codigo do cliente?: ")
    consultarV = consultar in cliente['cod']
    if consultarV:
        pos = cliente['cod'].index(consultar)
        print('------------ Informações Localizadas Com sucesso! ------------')
        print('')
        print("Codigo \t Nome \t\t Cidade \t Telefone")
        print("{0} \t {1} \t {2} \t {3}".format(cliente['cod'][pos], cliente['nome'][pos], cliente['cidade'][pos],
                                                cliente['telefone'][pos]))
        print('')
        novaConsultaCliente = input('\nDeseja realizar nova Consulta? 1.Sim ou 2.Menu Inicial:\n')
        if novaConsultaCliente == '1':
            consultaCliente()
        else:
            startsystem()
    else:
        exitConsultaCliente = input('\nCliente não Localizado!\nDeseja realizar nova Consulta? 1.Sim ou 2.Menu Inicial:\n')
        if exitConsultaCliente == '1':
            consultaCliente()
        else:
            startsystem()


def listaCliente():
    cls()
    print('---------- 3. LISTA DE CLIENTES -----------')
    print()
    print("Codigo \t Nome \t\t Telefone")

    for i in range(len(cliente['cod'])-1):
        print(f"  {cliente['cod'][i]} \t {cliente['nome'][i]}  \t {cliente['telefone'][i]}")
 
    print('')

    listavolta = 0
    while listavolta != '9':
        listavolta = input('DIGITE 9 MENU INICIAL: ')
        print('Digite somente as Opções do Menu: ')
        cls()
    else:
        startsystem()
        cls()
    print('')


def transDeposito() -> object:
    cls()
    print('---------- 3.1 REALIZANDO DEPÓSITO -----------')
    consultar = input("\nInforme o codigo da conta em que deseja realizar o deposito: ")
    consultarV = consultar in Contas['cod']

    if consultarV:

        pos = Contas['cod'].index(consultar)
        print()
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format(cliente['nome'][pos], Contas['saldo'][pos]))  #Buquei cliente no banco de dados e imprimi
        cls()
        deposito = input("\nInforme o valor do deposito: ")
        deposito = float(deposito)
        valor = Contas['saldo'][pos]
        valor = valor + deposito
        Contas['saldo'][pos] = valor
        print('Deposito realizado com Sucesso!!!')
        print()
        print('O seu SALDO atual é de: {},\nDeseja realizar outro Depósito?: '.format(Contas['saldo'][pos]))
        print('')
        print('1 - SIM: ')
        print('2 - MENU INICIAL: ')
        outroDep = '1', '2'
        while outroDep:
            outroDep = input('********* DIGITE A OPÇÃO DESEJADA : ')
            cls()
            if outroDep == '1':
                transDeposito()
            elif outroDep == '2':
                startsystem()
            print('Digite Somente as Opções do Menu: ')
    else:
        input("Conta nao existe!!")
        mdep = '''
Deseja Realizar outro Depósito?:
1 - SIM:
2 - Voltar:
'''
        print(mdep)
        outroDeps = '1', '2'
        while outroDeps:
            outroDep = input('DIGITE A OPÇÃO DESEJADA:__   ')
            if outroDep == '1':
                transDeposito()
            elif outroDep == '2':
                startsystem()
            print('Digite Somente as Opções do Menu: ')


def transSaque() -> object:
    cls()
    print('---------- 3.1 REALIZANDO SAQUE -----------')
    consultar = input("\nInforme o Numero da Conta-Corrente que deseja realizar o SAQUE: ")
    consultarV = consultar in Contas['cod']
    cls()
    if consultarV:
        pos = Contas['cod'].index (consultar)
        print ()
        print ('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format (cliente['nome'][pos],
                                                                                        Contas['saldo'][pos]))
        saque = input ("\nValor do saque R$:_ ")
        saque = float (saque)
        valor = Contas['saldo'][pos]
        if saque <= valor:
            valor -= saque
            Contas['saldo'][pos] = valor
            print('Olá {} tudo bem?, o Saldo atual da sua Conta-Corrente é de: {}'.format(cliente['nome'][pos],
                                                                                            Contas['saldo'][pos]))
        else:
            print('{} voce não tem saldo para realizar saque de R$ {}'.format(cliente['nome'][pos], saque))

        outroDep = '''
Digite 1 Para voltar ao Menu Inicial  

Digite 2 para novo Saque      
'''
        print(outroDep)
        while outroDep:
            outroDep = input('DIGITE AQUI: ')
            if outroDep == '1':
                startsystem()
            if outroDep == '2':
                transSaque()
            print('Opção Inválida ')

def transFerencia():
    print('MÉTODO - TRANSFERENCIA EM MANUTENÇÃO')
    menuTrans()
    print()

def transLista():  #extrato conta-corrente listar as transaçoes realizadas
    print('MÉTODO - LISTAR EM MANUTENÇÃO')
    menuTrans()
    print()

def contador():
    mensagem = '''
Deseja Realizar outro Cadastro?

1 - SIM
9 - VOLTAR
'''
    print(mensagem)
    listavolta = '1', '9'
    while listavolta:
        listavolta = input('DIGITE A OPÇÃO DESEJADA: ')
        if listavolta == '1':
            novoCliente()
        elif listavolta == '9':
            startsystem()
        print('Opção Inválida, Digite somente a Opção do Menu: ')


if __name__ == '__main__':
    startsystem()
