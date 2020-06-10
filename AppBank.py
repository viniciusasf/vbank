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
    print('Cliente Cadastrado com Sucesso!!!')
    print()
    print('Cliente: {}, \nSeu Codigo é: {}, \nConta-Corrente Numero: {} foi criado com Sucesso!!!!, \nDepósito inicial de R$: {}'.format(nome, cod, cc, depinicial))
    monta_menu(menu_principal)

def consultaCliente():
    print()
    print('------------------------- 2. CONSULTA CLIENTE ----------------------')
    consultar = input("\nQual o codigo do cliente?: ")
    consultarV = consultar in cliente['cod']
    if consultarV:
        pos = cliente['cod'].index(consultar)
        print('Cliente Localizado Com sucesso!')
        print('')
        print("Codigo \t Nome \t\t Cidade \t Telefone")
        print("  {0}    \t {1} \t {2} \t {3}".format(cliente['cod'][pos], cliente['nome'][pos], cliente['cidade'][pos],
                                                cliente['telefone'][pos]))
        print('')
        monta_menu(menu_principal)

    else:
        print('Cliente Não Localizado, tente novamente')
        monta_menu(menu_cadastro)

def listaCliente():
    print('---------- 3. LISTA DE CLIENTES -----------')
    print()
    print("Codigo \t Nome \t\t Telefone")

    for i in range(len(cliente['cod']) - 1):
        print(f"  {cliente['cod'][i]} \t {cliente['nome'][i]}  \t {cliente['telefone'][i]}")
        monta_menu(menu_principal)

def transDeposito() -> object:
    print('---------- 3.1 REALIZANDO DEPÓSITO -----------')
    consultar = input("\nInforme o codigo da conta em que deseja realizar o deposito: ")
    consultarV = consultar in Contas['cod']
    if consultarV:
        pos = Contas['cod'].index(consultar)
        print()
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format(cliente['nome'][pos], Contas['saldo'][pos]))  #Buquei cliente no banco de dados e imprimi
        deposito = float(input("\nInforme o valor do deposito: "))
        deposito = float(deposito)
        valor = Contas['saldo'][pos]
        valor = valor + deposito
        Contas['saldo'][pos] = valor
        print('Deposito realizado com Sucesso!!!')
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
        else:
            print('{} voce não tem saldo para realizar saque de R$ {}'.format(cliente['nome'][pos], saque))

def transFerencia():
    print('MÉTODO - TRANSFERENCIA EM MANUTENÇÃO')

def transLista():
    print('MÉTODO - LISTAR EM MANUTENÇÃO')

menu_cadastro = {
    '1': ('- Cadastrar', novoCliente),
    '2': ('- Consulta Cliente', consultaCliente),
    '3': ('- Visualizar todos Clietes', listaCliente),
    '9': ('- Deslogar', sair),
}
menu_trans = {
    '1': ('- Depósito', transDeposito),
    '2': ('- Saque', transSaque),
    '9': ('- Voltar', menu_cadastro),
}
menu_principal = {
    '1': ('- Cadastro', menu_cadastro),
    '2': ('- Transaçao', menu_trans),
    '9': ('- Deslogar', sair),
}
def monta_menu(menu) -> object:
    print()
    print('******* Sistema VBANK *******:')
    for k, v in menu.items():
        texto, _ = v
        print(k, texto)
    opcao = input('Digite a Opçao Desejada:    ')
    print('-' *30)
    try:
        escolhido = menu[opcao]
        _, funcao = escolhido
        if isinstance(funcao, dict):
            monta_menu(funcao)
        else:
            funcao()
    except KeyError:
        print('Opção Inválida Tente novamente')
        monta_menu(menu_principal)



if __name__ == '__main__':
    monta_menu(menu_principal)
