import sqlite3

class CategoriaDAO:
    
    
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        """
        Cria a tabela categoria com seus respectivos campos
        """
        
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                is_entrada INTEGER NOT NULL,
                is_saida INTEGER NOT NULL
            )
            '''
        )

    def insert(self, titulo, is_entrada, is_saida):
        """
        Insere uma nova categoria no banco de dados
        """
        
        self.conn.execute(
            '''
            INSERT INTO categorias (titulo, is_entrada, is_saida)
            VALUES (?, ?, ?)
            ''',
            (titulo, is_entrada, is_saida)
        )
        self.conn.commit()

    def get_categorias_entrada(self):
        """
        Puxa todas categorias de entrada do banco
        """
        cursor = self.conn.execute(
            '''
            SELECT id, titulo, is_entrada, is_saida
            FROM categorias WHERE is_entrada
            '''
        )
        return cursor.fetchall()
    
    def get_categorias_saida(self):
        """
        Puxa todas categorias de saida do banco
        """
        cursor = self.conn.execute(
            '''
            SELECT id, titulo, is_entrada, is_saida
            FROM categorias WHERE is_entrada
            '''
        )
        return cursor.fetchall()

    def get_by_id(self, id):
        """
        Puxa uma categoria específica do banco pelo ID
        """
        cursor = self.conn.execute(
            '''
            SELECT id, titulo, is_entrada, is_saida
            FROM categorias
            WHERE id=?
            ''',
            (id,)
        )
        return cursor.fetchone()

    def update(self, id, titulo, is_entrada, is_saida):
        """
        Atualiza uma categoria pelo ID
        """
        self.conn.execute(
            '''
            UPDATE categorias
            SET titulo=?, is_entrada=?, is_saida=?
            WHERE id=?
            ''',
            (titulo, is_entrada, is_saida, id)
        )
        self.conn.commit()

    def delete(self, id):
        """
        Delete uma categoria do banco
        """
        self.conn.execute(
            '''
            DELETE FROM categorias
            WHERE id=?
            ''',
            (id,)
        )
        self.conn.commit()