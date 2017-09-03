from model_.realizadomodel import Realizado

from connection.connection import db
from model.gastomodel import Gasto


class CreateTables:
    db.drop_tables([Gasto, Realizado])
    db.create_tables([Gasto, Realizado], safe=True)

    with db.atomic():
        Gasto.insert_many([
            {"id": 1, "descricao_previsto": "Teste", "valor_previsto": 11.2, "total_realizado": 8, "saldo": 4},
            {"id": 2, "descricao_previsto": "Teste 2", "valor_previsto": 14, "total_realizado": 7.5, "saldo": 6.5},
            {"id": 3, "descricao_previsto": "Teste 3", "valor_previsto": 20, "total_realizado": 10, "saldo": 10}
        ]).execute()

    with db.atomic():
        Realizado.insert_many([
            {"id": 1, "descricao": "Teste Realizado 1", "valor": 100.00, "gasto": 1},
            {"id": 2, "descricao": "Teste Realizado 2", "valor": 220.22, "gasto": 1},
            {"id": 3, "descricao": "Teste Realizado 3", "valor": 221.10, "gasto": 1},
            {"id": 4, "descricao": "Teste Realizado 4", "valor": 560.00, "gasto": 2},
            {"id": 5, "descricao": "Teste Realizado 5", "valor": 212.00, "gasto": 3},
            {"id": 6, "descricao": "Teste Realizado 6", "valor": 10.00, "gasto": 2},
            {"id": 7, "descricao": "Teste Realizado 7", "valor": 22.00, "gasto": 3},
            {"id": 8, "descricao": "Teste Realizado 8", "valor": 20.10, "gasto": 1},
            {"id": 9, "descricao": "Teste Realizado 9", "valor": 20.01, "gasto": 2},
            {"id": 10, "descricao": "Teste Realizado 10", "valor": 29.01, "gasto": 3}
        ]).execute()
