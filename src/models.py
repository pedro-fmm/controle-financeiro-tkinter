import sqlite3

from datetime import date
from datetime import timedelta

class Transacao:
    def __init__(self, id, titulo, valor, data, is_saida):
        self.id = id
        self.titulo = titulo
        self.valor = valor
        self.data = data
        self.is_saida = is_saida


class TransacaoDAO:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            valor REAL,
            data TEXT,
            is_saida INTEGER
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def get_saldo(self):
        query = '''
        SELECT SUM(valor) FROM transacoes WHERE is_saida
        '''
        self.cursor.execute(query)
        debitos = self.cursor.fetchone()[0]
        
        query = '''
        SELECT SUM(valor) FROM transacoes WHERE NOT(is_saida) 
        '''
        self.cursor.execute(query)
        creditos = self.cursor.fetchone()[0]
        
        if creditos == None:
            creditos = 0
        if debitos == None:
            debitos = 0
        saldo = creditos - debitos
        return saldo


    def insert_transacao(self, transacao):
        query = '''
        INSERT INTO transacoes (titulo, valor, data, is_saida)
        VALUES (?, ?, ?, ?)
        '''
        values = (transacao.titulo, transacao.valor, transacao.data, transacao.is_saida)
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_transacoes(self):
        query = '''
        SELECT * FROM transacoes ORDER BY data DESC
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        transacoes = []
        for row in rows:
            id, titulo, valor, data, is_saida = row
            transacao = Transacao(id, titulo, valor, data, is_saida)
            transacoes.append(transacao)

        return transacoes
    
    def get_all_entradas(self):
        query = '''
        SELECT * FROM transacoes WHERE NOT(is_saida) ORDER BY data DESC
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        transacoes = []
        for row in rows:
            id, titulo, valor, data, is_saida = row
            transacao = Transacao(id, titulo, valor, data, is_saida)
            transacoes.append(transacao)

        return transacoes

    def get_all_saidas(self):
        query = '''
        SELECT * FROM transacoes WHERE is_saida ORDER BY data DESC
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        transacoes = []
        for row in rows:
            id, titulo, valor, data, is_saida = row
            transacao = Transacao(id, titulo, valor, data, is_saida)
            transacoes.append(transacao)

        return transacoes

    def update_transacao(self, transacao):
        query = '''
        UPDATE transacoes SET titulo=?, valor=?, data=?, is_saida=? WHERE id=?
        '''
        values = (transacao.titulo, transacao.valor, transacao.data, transacao.is_saida, str(transacao.id))
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_transacao(self, id):
        query = '''
        DELETE FROM transacoes WHERE id=?
        '''
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def get_transacoes_graph(self, meses, tipo):
        data_atual = date.today()
        data_anterior = data_atual - timedelta(days=int(meses)*30)
        tipo = 0 if tipo == "Entrada" else 1

        query = '''
        SELECT * FROM transacoes WHERE is_saida=? AND data BETWEEN ? AND ? ORDER BY data DESC
        '''
        values = (tipo, data_anterior, data_atual)
        self.cursor.execute(query, values)
        rows = self.cursor.fetchall()

        if int(meses) == 1:
            transacoes = {"valores": [], "datas": []}
            for row in rows:
                id, titulo, valor, data, is_saida = row
                transacoes["valores"].append(valor)
                transacoes["datas"].append(data.split("-")[2])
        else:
            transacoes = {}
            for row in rows:
                id, titulo, valor, data, is_saida = row
                if not transacoes.get(data.split("-")[1], False):
                    transacoes[data.split("-")[1]] = valor
                else:
                    transacoes[data.split("-")[1]] += valor
        return transacoes

    def close(self):
        self.cursor.close()
        self.conn.close()
