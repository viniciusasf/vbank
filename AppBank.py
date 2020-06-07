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

def consultaCep():

    cep_input = input('Digite o CEP para a consulta: ')

    if len(cep_input) != 8:
        option1 = int(input('CEP Inválido, Deseja realizar uma nova consulta ?\n1. Sim\n2. Sair\n'))
        if option1 == '1':
            consultaCep()
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



def novoCliente():
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

def consultaCliente():
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
        conCliente = '''
Deseja realizar nova Consulta?
1 - Sim
2 - Voltar
'''
        print(conCliente)
        conCliente = '1', '2'
        while conCliente:
            consultaCliente()
        else:
            monta_menu()

    else:
        exitConsultaCliente = input('\nCliente não Localizado!\nDeseja realizar nova Consulta? 1.Sim ou 2.Menu Inicial:\n')
        if exitConsultaCliente == '1':
            consultaCliente()

    monta_menu()

def listaCliente():

    print('---------- 3. LISTA DE CLIENTES -----------')
    print()
    print("Codigo \t Nome \t\t Telefone")

    for i in range(len(cliente['cod'])-1):
        print(f"  {cliente['cod'][i]} \t {cliente['nome'][i]}  \t {cliente['telefone'][i]}")
    conCliente = '''
Digite para 9 - Voltar
'''
    print(conCliente)
    conCliente = '9'
    while conCliente:
        monta_menu()
    else:
        print('Opçao Inválida')


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
    else:
        print("Conta nao existe!!")

def transSaque() -> object:
    print('---------- 3.1 REALIZANDO SAQUE -----------')
    consultar = input("\nInforme o Numero da Conta-Corrente que deseja realizar o SAQUE: ")
    consultarV = consultar in Contas['cod']
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
            print('Olá {} tudo bem?, o Saldo atual da sua Conta-Corrente é de R$: {}'.format(cliente['nome'][pos],
                                                                                            Contas['saldo'][pos]))

        else:
            print('{} voce não tem saldo para realizar saque de R$ {}'.format(cliente['nome'][pos], saque))


def transFerencia():
    print('MÉTODO - TRANSFERENCIA EM MANUTENÇÃO')


def transLista():  #extrato conta-corrente listar as transaçoes realizadas
    print('MÉTODO - LISTAR EM MANUTENÇÃO')


menu_cadastro = {
    '1': ('Cadastrar', novoCliente),
    '2': ('Consulta Cliente', consultaCliente),
    '3': ('Visualizar todos Clietes', listaCliente),
}

menu_trans = {
    '1': ('- Depósito', transDeposito),

    '2': ('- Saque', transSaque),

}
menu_principal = {
    '1': ('- Cadastro', menu_cadastro),

    '2': ('- Transaçao', menu_trans)
}

def monta_menu(menu):
    print()
    print('Sistema VBANK - Conta Corrente:')
    for k, v in menu.items():
        texto, _ = v
        print(k, texto)
    opcao = input('Digite a Opçao Desejada: ')
    print('-' *30)
    escolhido = menu[opcao]
    _, funcao = escolhido

    if isinstance(funcao, dict):
        monta_menu(funcao)
    else:
        funcao()


if __name__ == '__main__':
    monta_menu(menu_principal)
