#Tarefas:
# 1 lista de clientes;
# 2 fazer novos testes;
# 3 implementar a função transaque, transferencia, translista e listaCliente;
import requests


Contas = dict(cod=[], saldo=[], tr=[])
cliente = dict(cod=[], nome=[], cidade=[], telefone=[], cc=[], address_data=[])
Trans = dict(cod=[], tipo=[], origem=[], destino=[], valor=[])
numClientes = 0

def startsystem():
    print('')
    print('--------------- 1 - MENU INICIAL ---------------')
    print('')
    print('1 - CADASTRO DE CLIENTE')  #todo menu de criação de cliente está OK
    print('2 - REALIZAR TRANSAÇÃO')  #entra no menu de transação OK
    print('9 - SAIR')
    starSystem = input('--> DIGITE A OPÇÃO DESEJADA:__   ')
    print()
    if starSystem == '1':
        menuCliente()
    if starSystem == '2':
        menuTrans()
    else:
        print('Oção Inválida!')


def menuCliente():
    print('------------- 2 - MENU CLIENTE ----------------')  #todo menu de criação de cliente está OK
    print('')
    print('1 - CADASTRO')
    print('2 - CONSULTA')
    print('3 - LISTAR DE CLIENTES')
    print('9 - VOLTAR')
    menuCli = input('--> DIGITE A OPÇÃO DESEJADA:__   ')
    if menuCli == '1':
        novoCliente()
    if menuCli == '2':
        consultaCliente()
    if menuCli == '3':
        listaCliente()
    if menuCli == '9':
        startsystem()


def menuTrans():
    print('--------------- 3 - TRANSAÇÕES ----------------')
    print("")
    print("1 - DEPOSITO")  #inicia o deposito normalmente. OK
    print("2 - SAQUE")
    print("3 - TRANSFERENCIA")
    print("4 - IMPRIMIR LISTA TRANSAÇÕES")
    print("5 - VOLTAR")
    trans = input('--> DIGITE A OPÇÃO DESEJADA:__   ')
    if trans == '1':
        transDeposito()
    if trans == '2':
        transSaque()
    if trans == '3':
        transFerencia()
    if trans == '4':
        transLista()


def consultaCep():  # <------ Consulta API Correios para busca de CEP
    print('---------------------------')
    print('----- Consulta CEP --------')
    print('---------------------------')
    print()

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
    # ----------- ("NOVO")Função Inserir novo Cliente, cria conta corrente e deposita valor inicial ---------------
    print()
    print('------- 1 - CADASTRO CLIENTE / C.C ---------------')
    print()
    cod = input('CODIGO DO CLIENTE: ')
    nome = input('NOME: ')
    print('DESEJA CONSULTAR O CEP: ?')
    cep = input('DIGITE 1. PARA SIM\n2. Continue...')
    if cep == '1':
        consultaCep()
    else:
        telefone = input('TELEFONE: ')
        cidade = input('CIDADE:')
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
        print('Cliente: {}, Conta-Corrente Numero: {} foi criado com Sucesso!!!!, depósito inicial de: {}'.format(nome, cc, depinicial))
        print('')
        print('DESEJA CADASTRAR OUTRO CLIENTE?: ')
        print('1 - SIM: ')
        print('2 - VOLTAR: ')
        outroCli = input('--> DIGITE A OPÇÃO DESEJADA:__   ')
        if outroCli == '1':
            novoCliente()
        else:
            startsystem()
    print('-')


def consultaCliente():  # ----------- ("NOVO")Função Consultar novo Cliente ---------------

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
    print("Codigo \t Nome \t\t Telefone \t Conta \t Saldo")
    pos = cliente
    print(pos)


def transDeposito() -> object:
    print()
    print('---------- 3.1 REALIZANDO DEPÓSITO -----------')
    consultar = input("\nInforme o codigo da conta em que deseja realizar o deposito: ")
    consultarV = consultar in Contas['cod']

    if consultarV:

        pos = Contas['cod'].index(consultar)
        print()
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format(cliente['nome'], Contas['saldo']))  #Buquei cliente no banco de dados e imprimi
        deposito = input("\nInforme o valor do deposito: ")
        deposito = float(deposito)
        valor = Contas['saldo'][pos]
        valor = valor + deposito
        Contas['saldo'][pos] = valor
        print('Deposito realizado com Sucesso!!!')
        print('O seu SALDO atual é de: {}, deseja realizar outro Depósito?: '.format(Contas['saldo']))
        print('')
        print('1 - SIM: ')
        print('2 - MENU INICIAL: ')
        outroDep = input('********* DIGITE A OPÇÃO DESEJADA: ')
        if outroDep == '1':
            transDeposito()
        else:
            startsystem()

    else:
        input("Conta nao existe!!")

        print('Deseja Realizar outro Depósito?: ')
        print('1 - SIM: ')
        print('2 - Voltar: ')
        outroDep = input('--> DIGITE A OPÇÃO DESEJADA:__   ')
        if outroDep == '1':
            transDeposito()
        else:
            startsystem()


def transSaque():
    consultar = input("\nInforme o codigo da conta em que deseja realizar o saque: ")
    consultarV = consultar in Contas['cod']

    if consultarV == True:

        pos = Contas['cod'].index(consultar)
        saque = input("\nInforme o valor do saque: ")
        saque = float(saque)
        valor = Contas['saldo'][pos]

        if valor > saque:  # INSERIR UMA VALIDAÇÃO DE LIMITE ()
            valor = valor - saque
            Contas['saldo'][pos] = valor

        else:
            input("Saldo insuficiente!!")

    else:
        input("Conta nao existe!!")

def transFerencia():
    print('MÉTODO - TRANSFERENCIA EM MANUTENÇÃO')
    menuTrans()
    print()

def transLista():
    print('MÉTODO - LISTAR EM MANUTENÇÃO')
    menuTrans()
    print()




# def main():
#     pass
#

if __name__ == '__main__':
    startsystem()
