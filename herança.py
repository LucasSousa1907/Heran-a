class Conta:
    def __init__(self, numero, titular, saldo=0.0):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo

    def __str__(self):
        return f'Conta {self.numero} - Titular: {self.titular} - Saldo: R$ {self.saldo:.2f}'

    def creditar(self, valor):
        self.saldo += valor

    def debitar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        return False



class ContaCorrente(Conta):
    def __init__(self, numero, titular, saldo=0.0, limite=500):
        super().__init__(numero, titular, saldo)
        self.limite = limite

    def debitar(self, valor):
        if self.saldo + self.limite >= valor:
            self.saldo -= valor
            return True
        return False

    def __str__(self):
        return (f'Conta Corrente {self.numero} - Titular: {self.titular} '
                f'- Saldo: R$ {self.saldo:.2f} - Limite: R$ {self.limite:.2f}')


class ContaPoupanca(Conta):
    def __init__(self, numero, titular, saldo=0.0, rendimento=0.005):
        super().__init__(numero, titular, saldo)
        self.rendimento = rendimento

    def aplicar_rendimentos(self):
        ganho = self.saldo * self.rendimento
        self.saldo += ganho

    def __str__(self):
        return (f'Conta Poupança {self.numero} - Titular: {self.titular} '
                f'- Saldo: R$ {self.saldo:.2f} - Rendimento: {self.rendimento * 100:.2f}%')


class Banco:
    def __init__(self):
        self.contas = []

    def cadastrar(self, conta):
        if self.procurar_conta(conta.numero):
            print('Já existe uma conta com esse número.')
        else:
            self.contas.append(conta)
            print('Conta cadastrada com sucesso.')

    def procurar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

    def creditar(self, numero, valor):
        conta = self.procurar_conta(numero)
        if conta:
            conta.creditar(valor)
            print(f'Crédito de R$ {valor:.2f} realizado na conta {numero}')
        else:
            print('Conta não encontrada.')

    def debitar(self, numero, valor):
        conta = self.procurar_conta(numero)
        if conta:
            if conta.debitar(valor):
                print(f'Débito de R$ {valor:.2f} realizado na conta {numero}')
            else:
                print('Saldo insuficiente.')
        else:
            print('Conta não encontrada.')

    def saldo(self, numero):
        conta = self.procurar_conta(numero)
        if conta:
            print(f'Saldo da conta {numero}: R$ {conta.saldo:.2f}')
        else:
            print('Conta não encontrada.')

    def transferir(self, origem, destino, valor):
        conta_origem = self.procurar_conta(origem)
        conta_destino = self.procurar_conta(destino)

        if not conta_origem or not conta_destino:
            print('Conta de origem ou destino não encontrada')
            return

        if not conta_origem.debitar(valor):
            print('Saldo insuficiente para transferência')
            return

        conta_destino.creditar(valor)
        print(f'Transferência de R$ {valor:.2f} realizada de {origem} para {destino}')



def menu():
    banco = Banco()

    while True:
        print('\n=== MENU DO BANCO ===')
        print('1 - Cadastrar Conta Corrente')
        print('2 - Cadastrar Conta Poupança')
        print('3 - Consultar saldo')
        print('4 - Creditar valor')
        print('5 - Debitar valor')
        print('6 - Transferir valor')
        print('7 - Aplicar rendimento (somente poupança)')
        print('8 - Listar todas as contas')
        print('0 - Sair')

        opcao = input('Escolha uma opção: ')

        if opcao in ['1', '2']:
            numero = int(input('Número da conta: '))
            titular = input('Nome do titular: ')
            saldo_inicial = float(input('Saldo inicial: '))

            if opcao == '1':
                limite = float(input('Limite da conta corrente: '))
                conta = ContaCorrente(numero, titular, saldo_inicial, limite)

            else:  # opção 2
                rendimento = float(input('Rendimento (ex: 0.005 para 0.5%): '))
                conta = ContaPoupanca(numero, titular, saldo_inicial, rendimento)

            banco.cadastrar(conta)

        elif opcao == '3':
            numero = int(input('Número da conta: '))
            banco.saldo(numero)

        elif opcao == '4':
            numero = int(input('Número da conta: '))
            valor = float(input('Valor a creditar: '))
            banco.creditar(numero, valor)

        elif opcao == '5':
            numero = int(input('Número da conta: '))
            valor = float(input('Valor a debitar: '))
            banco.debitar(numero, valor)

        elif opcao == '6':
            origem = int(input('Conta de origem: '))
            destino = int(input('Conta de destino: '))
            valor = float(input('Valor da transferência: '))
            banco.transferir(origem, destino, valor)

        elif opcao == '7':
            numero = int(input('Número da conta poupança: '))
            conta = banco.procurar_conta(numero)
            if isinstance(conta, ContaPoupanca):
                conta.aplicar_rendimentos()
                print('Rendimento aplicado com sucesso!')
            else:
                print('Essa conta não é uma conta poupança.')

        elif opcao == '8':
            if not banco.contas:
                print('Nenhuma conta cadastrada')
            else:
                for conta in banco.contas:
                    print(conta)

        elif opcao == '0':
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida. Tente novamente')


if __name__ == '__main__':
    menu()
