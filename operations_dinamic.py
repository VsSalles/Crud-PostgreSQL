import psycopg2

class PostgreSqlOperations:
    def __init__(self, name='crud_python', user='postgres', host='localhost', port=5433, password='Inovepg123'):
        self.name = name
        self.host = host
        self.port = port
        self.password = password
        self.user = user
    
    def __connect(self):
        self.conn = psycopg2.connect(database=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        return self.conn
    
    def close_db(self):
        self.conn.close()

    def get_cursor(self):
        conn = self.__connect()
        self.cursor = conn.cursor()
        return self.cursor

    def list_all(self, tabela):
        cursor = self.get_cursor()
        cursor.execute(f"SELECT * FROM {tabela};")
        data = cursor.fetchall()

        if len(data) > 0:
            print(f'Listando dados da tabela:{tabela}')
            print(100*'-')
            for dado in data:
                print(f'registro:{dado}')
                print(100*'-')
            self.close_db()
        else:
            print(f'Não existe dados cadastrado na tabela:{tabela}')
            self.close_db()

    def insert(self, tabela, colunas, *values): #args = colunas e valores das colunas EM ORDEM
        cursor = self.get_cursor()
        try:
            pedaco_sql = f'INSERT INTO {tabela} ('
            for coluna in colunas:
                pedaco_sql += f'{coluna}, '

            outro_pedaco_sql = f') VALUES {values}'
            sql = pedaco_sql + outro_pedaco_sql

            print(sql[50])


            #cursor.execute(sql)
            #self.conn.commit()
            #print('Dados cadastrados com successo')
            #self.close_db()
        except Exception as e:
            print(f'Erro ao cadastrar: {e}')
            self.close_db()
       

    def update(self, tabela,  *args, id):
        cursor = self.get_cursor()
        try:
            for dados in args:
                cursor.execute(f"UPDATE {tabela} SET {args[dados]}={args[dados]}, WHERE id={id}")
            print('Dados atualizados com sucesso')
            self.conn.commit()
            self.close_db()
        except Exception as e:
            print(f'ocorreu um erro ao atualizar:{e}')
            self.close_db()
        
    def delete(self, tabela, id):
        cursor = self.get_cursor()
        try:
            if not self.list_one(id, tabela):
                return False
            cursor.execute(f"DELETE FROM {tabela} WHERE id={id}")
            print('Dado delatado com sucesso')
            self.conn.commit()
            self.close_db()
        except Exception as e:
            print(f'ocorreu um erro ao deletar:{e}')
            self.close_db()
    
    def list_one(self, id, tabela):
        cursor = self.get_cursor()
        try:
            cursor.execute(f"SELECT * FROM {tabela} WHERE id={id}")
            dado = cursor.fetchone()
            if not dado:
                return print('dado não existe')
            print('Dado deletado com sucesso')
            self.close_db()
        except Exception as e:
            print(f'erro ao buscar dado:{e}')

if __name__ == '__main__':
    crud = PostgreSqlOperations()   
    crud.insert('produtos', ['nome', 'preco', 'estoque'], 'carro', 15000, 1)
