from models import Conta, engine, Status, Bancos, Historico, Tipos
from sqlmodel import Session, select
from datetime import date

def criar_conta(conta: Conta):
    with Session(engine) as session: 
        statement = select(Conta).where(Conta.banco == conta.banco)
        results = session.exec(statement).all()

        if results:
            print('Já existe uma conta nesse banco.')
            return

        session.add(conta)
        session.commit()
        return conta

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first()

        if not conta:
            raise ValueError("Conta não encontrada.")

        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo.')

        conta.status = Status.INATIVO
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_saida)
        conta_saida = session.exec(statement).first()

        if not conta_saida:
            raise ValueError("Conta de saída não encontrada.")

        if conta_saida.status != Status.ATIVO:
            raise ValueError("A conta de saída não está ativa.")

        if conta_saida.valor < valor:
            raise ValueError('Saldo insuficiente.')

        statement = select(Conta).where(Conta.id == id_conta_entrada)
        conta_entrada = session.exec(statement).first()

        if not conta_entrada:
            raise ValueError("Conta de entrada não encontrada.")

        if conta_entrada.status != Status.ATIVO:
            raise ValueError("A conta de entrada não está ativa.")


        conta_saida.valor -= valor
        conta_entrada.valor += valor
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:

        if historico.valor is None or historico.valor <= 0:
            raise ValueError("O valor da movimentação deve ser maior que zero.")

        # Busca a conta associada ao histórico
        statement = select(Conta).where(Conta.id == historico.conta_id)
        conta = session.exec(statement).first()

        if not conta:
            raise ValueError("Conta não encontrada.")

        # Verifica se a conta está ativa
        if conta.status != Status.ATIVO:
            raise ValueError("A conta não está ativa.")


        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        else:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente.")
            conta.valor -= historico.valor

        session.add(historico)
        session.commit()
        return historico


historico = Historico(conta_id=1, tipo=Tipos.ENTRADA, valor=10, data=date.today())
movimentar_dinheiro(historico)