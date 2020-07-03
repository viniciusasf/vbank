import pickle
import sys
import os
from time import sleep
from tabulate import tabulate


if os.path.getsize('data.pickle') > 0:
    with open('data.pickle', 'rb') as p:
        unpickler = pickle.Unpickler(p)
        data = unpickler.load()
else:
    data = dict()


Contas = dict(cod=[], saldo=[], tr=[])
Cliente = dict(cod=[], nome=[], cidade=[], telefone=[])
Trans = dict(codtransConta=[], codigotransacao=[], tipo=[], origem=[], destino=[], valor=[])


if data.get('Contas'):
    Contas = data.get('Contas')
if data.get('Cliente'):
    Cliente = data.get('Cliente')
if data.get('Trans'):
    Trans = data.get('Trans')


def sair():
    print('Encerrando o sistema. \nAguarde...\nGravando Dados no Bando de Dados...')
    contagem()
    data = dict(Contas=Contas, Cliente=Cliente, Trans=Trans)
    with open('data.pickle', 'wb') as p:
        pickle.dump(data, p)
    print('Sistema Encerrado')
    sys.exit()


def novoCliente():
    print('------- 1 - CADASTRO CLIENTE / C.C ---------------\n')
    cod = input('CODIGO DO CLIENTE: ').strip()
    nome = input('NOME: ').strip()
    cidade = input('CIDADE: ').strip()
    telefone = input('TELEFONE: ').strip()
    cc = input('Nº CONTA-CORRENTE: ').strip()
    codtransConta = input('CODIGO DE TRANSAÇÃO: ').strip()
    depinicial = input('DEPÓSITO INICIAL: ').strip()
    depinicial = float(depinicial)
    Cliente['cod'].append(cod)
    Cliente['nome'].append(nome)
    Cliente['cidade'].append(cidade)
    Cliente['telefone'].append(telefone)
    Contas['cod'].append(cc)
    Trans['codtransConta'].append(codtransConta)
    Contas['saldo'].append(depinicial)
    print('Cliente e Conta-Corrente Cadastrados com Sucesso!!!')
    print('Nome do Cliente: {} \nSeu Codigo é: {} \nConta-Corrente Numero: {} \nCodigo de Transação {} \nDepósito inicial de R$: {}'.format(nome, cod, cc, codtransConta, depinicial))
    monta_menu(menu_principal)


def consultaCliente():
    print('--------------- 2. CONSULTA CLIENTE ---------------\n')
    consultar = input("INFORME O CÓDIGO DO CLIENTE: ")
    consultarV = consultar in Cliente['cod']
    if consultarV:
        pos = Cliente['cod'].index(consultar)
        v = Cliente['cod'][pos], Cliente['nome'][pos], Cliente['cidade'][pos], Cliente['telefone'][pos]
        print('Cliente Localizado Com sucesso!\n')
        print(tabulate(v, headers=['codigo', "Nome", "Cidade", "Telefone"]))
        monta_menu(menu_principal)
    else:
        print('Cliente Não Localizado, tente novamente\n')
        monta_menu(menu_cadastro)


def imprime_clientes():
    print('CLIENTES')
    print(tabulate(Cliente, headers=['codigo', "Nome", "cidade", "telefone"], tablefmt="grid"))
    numeroclientes = len(Cliente['cod'])
    if numeroclientes >= 2:
        print('* {} CLIENTES LOCALIZADOS COM SUCESSO *'.format(numeroclientes))
        monta_menu(menu_principal)
    else:
        print('* {} CLIENTE LOCALIZADO COM SUCESSO *'.format(numeroclientes))
        monta_menu(menu_principal)


def transDeposito() -> object:
    print('---------- 3.1 REALIZANDO DEPÓSITO -----------')
    transcontasaque = input("\nInforme o Numero da Conta-Corrente que deseja DEPOSITAR: ")
    if transcontasaque in Trans['codtransConta']:
        pos1 = Trans['codtransConta'].index(transcontasaque)
        print ('Bem Vindo {} o seu SALDO é de R$ {}'.format(Cliente['nome'][pos1], Contas['saldo'][pos1]))
        Trans['codtransConta'] = pos1
        deposito = float(input("\nInforme o valor do deposito: "))
        deposito = float(deposito)
        valor = Contas['saldo'][pos1]
        valor = valor + deposito
        Contas['saldo'][pos1] = valor
        print('Deposito realizado com Sucesso!!!\n')
        print('{} \nSaldo atual da Conta é de R$: {}'.format(Contas['saldo'][pos1]))
        print('O Comprovante de seu Depósito é: {}'.format(Trans['codigotransacao']))
        monta_menu(menu_principal)

    else:
        print("Conta não Localizada!!")
        monta_menu(menu_principal)


def transSaque() -> object:
    print ('-' * 30)
    print ('{:^30}'.format('BANCO VBank'))
    print ('{:^30}'.format('SAQUE'))
    print ('-' * 30)
    consultar = input("\nInforme o Numero da Conta-Corrente que deseja realizar o SAQUE: ")
    consultarV = consultar in Contas['cod']
    if consultarV:
        pos = Contas['cod'].index(consultar)
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format(Cliente['nome'][pos],
                                                                                        Contas['saldo'][pos]))

        saque = int(input("Digite o valor do SAQUE R$: "))
        cedulas(saque)
        input('Precione ENTER para Confirmar o SAQUE')
        saque = float(saque)
        valor = Contas['saldo'][pos]
        if saque <= valor:
            valor -= saque
            Contas['saldo'][pos] = valor
            print ('{}, o Saldo atual da sua Conta-Corrente é de R$: {}'.format(Cliente['nome'][pos],
                                                                                 Contas['saldo'][pos]))
            monta_menu(menu_principal)
        else:
            print ('{} voce não tem saldo para realizar saque de R$ {}'.format(Cliente['nome'][pos], saque))
            monta_menu (menu_trans)


def cedulas(saque):
    print('\nContando CÉDULAS... Aguarde')
    contagem()
    print()
    print('Cédulas Disponíveis\n')
    notas = [100, 50, 20, 10, 5, 1]
    notas.sort()
    notas.reverse()
    numNotas = []
    for i in notas:
        numNotas.append(saque / i)
        saque %= i
    for i in range(len(notas)):
        zero = list(filter(lambda x: x != 0, numNotas[i]))
        print(f"Notas de %d = %d" % (notas[i], zero[i],))


def transFerencia():
    print('---------- TRANSFERENCIA -----------')
    transcontasaque = input("\nInforme o Numero da Conta-Corrente que deseja SACAR: ")
    if transcontasaque in Trans['codtransConta']:
        pos1 = Trans['codtransConta'].index(transcontasaque)
        print('Bem Vindo {} o seu SALDO é de R$ {}'.format(Cliente['nome'][pos1], Contas['saldo'][pos1]))
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
                print('O titular da Conta-Corrente é {}'.format(Cliente['nome'][pos2]))
                Contas['saldo'][pos1] = Contas['saldo'][pos1] - transferevalor
                Contas['saldo'][pos2] = Contas['saldo'][pos2] + transferevalor
                print('{} o saldo atual da sua Conta-Corrente é R$ {}'.format(Cliente['nome'][pos1], Contas['saldo'][pos1]))
                monta_menu(menu_principal)
            else:
                print('Conta Corrente não Localizada')
                monta_menu(menu_principal)
    else:
        print('Conta Corrente Não Localizada')
        monta_menu(menu_principal)


def pagamentos():
    print('---------- PAGAMENTOS -----------')
    consultar = input ("\nInforme o Numero da Conta-Corrente que deseja realizar utilizar para PAGAMENTO: \n")
    if consultar in Contas['cod']:
        cc = Contas['cod'].index(consultar)
        print('Olá {} tudo bem?, \nSaldo atual da sua Conta-Corrente é de: {}'.format(Cliente['nome'][cc],
                                                                                        Contas['saldo'][cc]))

        selecpag = '''
Selecione o Pagamento:
1 - ÁGUA
10 - CANCELAR OPÇÕES
'''
        print(selecpag)
        selecpag = input('Digite a opção Desejada: ')
        if selecpag == '1' or '10':
            if selecpag == '1':
                print('------ PAGAMENTO DE CONTAS ------\n')
                pagconta = float(input('Qual o valor do PAGAMENTO: '))
                if pagconta <= Contas['saldo'][cc]:
                    Contas['saldo'][cc] -= pagconta
                    print('Conta PAGA Com Sucesso\n')
                    print('{} o Saldo Atual de Sua Conta-Corrente é R$ {}'.format(Cliente['nome'][cc], Contas['saldo'][cc]))
                    monta_menu(menu_principal)
                else:
                    print('Não existe Saldo Disponível para Pagamento de Água\n')
                    monta_menu(menu_principal)
        else:
            print('Opção Inválida, Tente Novamente\n')
            pagamentos()
    else:
        print('Conta-Corrente não localizada')


def contagem():
    for cont in range(3, -1, -1):
        print(cont,'... ', end='')
        sleep(1)


menu_cadastro = {
    '1': ('- Cadastro', novoCliente),
    '2': ('- Consulta', consultaCliente),
    '3': ('- Lista', imprime_clientes),
    '9': ('- Deslogar', sair),
}
menu_trans = {
    '1': ('- Depósito', transDeposito),
    '2': ('- Saque', transSaque),
    '3': ('- Transferência', transFerencia),
    '4': ('- Pagamentos', pagamentos),
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
        print()
        monta_menu(menu_principal)


if __name__ == '__main__':
    monta_menu(menu_principal)
