from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Categoria

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/meu_banco"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def seed_categorias():
    categorias_data = [
        # Débito
        (1, 'Moradia', ["Aluguel", "Condomínio", "Conta de luz",
         "Conta de água", "Internet"], 'Débito'),
        (2, 'Transporte', [
         "Combustível", "Transporte público", "Manutenção veículo"], 'Débito'),
        (3, 'Alimentação', ["Supermercado",
         "Restaurante", "Lanches"], 'Débito'),
        (4, 'Saúde', ["Consultas médicas",
         "Medicamentos", "Planos de saúde"], 'Débito'),
        (5, 'Educação', ["Mensalidade escolar",
         "Cursos", "Livros e materiais"], 'Débito'),
        (6, 'Lazer', ["Viagens", "Cinema/teatro",
         "Assinaturas de streaming"], 'Débito'),
        (7, 'Impostos', ["IPTU", "IPVA", "Imposto de renda"], 'Débito'),
        (8, 'Outros (Débito)', ["Presentes",
         "Doações", "Taxas bancárias"], 'Débito'),

        # Crédito
        (9, 'Salário', ["Salário mensal", "Bônus", "13º salário"], 'Crédito'),
        (10, 'Investimentos', [
         "Rendimentos", "Venda de ações", "Aluguel de imóveis"], 'Crédito'),
        (11, 'Vendas', ["Venda de produto",
         "Prestação de serviço"], 'Crédito'),
        (12, 'Reembolsos', ["Despesas reembolsadas", "Seguro"], 'Crédito'),
        (13, 'Outros (Crédito)', ["Doações recebidas",
         "Aposentadoria", "Pensão"], 'Crédito'),

        # Transferência
        (14, 'Transferência entre contas', [
         "Conta corrente para poupança", "Poupança para conta corrente"], 'Transferência'),

        # Estorno
        (15, 'Estorno de pagamento', [
         "Devolução compra cartão", "Reversão TED/PIX"], 'Estorno'),

        # Ajuste
        (16, 'Ajustes financeiros', [
         "Correção de saldo", "Lançamento manual por erro"], 'Ajuste'),

        # Juros/Encargos
        (17, 'Juros e encargos', [
         "Juros empréstimo", "Multa por atraso", "Tarifa bancária"], 'Juros/Encargos'),

        # Depósito
        (18, 'Depósitos', ["Depósito em espécie",
         "Depósito via cheque"], 'Depósito'),

        # Saque
        (19, 'Saques', ["Saque caixa eletrônico",
         "Retirada na boca do caixa"], 'Saque'),

        # Pagamento Parcial
        (20, 'Pagamentos parciais', [
         "Parcial fatura cartão", "Parcial dívida fornecedor"], 'Pagamento Parcial'),

        # Troca/Compensação
        (21, 'Troca/compensação', ["Quitação com produto",
         "Serviço em troca de crédito"], 'Troca/Compensação')
    ]

    categorias = [
        Categoria(id=cat[0], category=cat[1], subcategorys=cat[2], type=cat[3])
        for cat in categorias_data
    ]

    session.bulk_save_objects(categorias)
    session.commit()
    print("✅ Categorias inseridas com sucesso!")


if __name__ == "__main__":
    seed_categorias()
