import psycopg2

class PostgreSqlOperations:
    def __init__(self, name='crud_python', user='postgres', host='localhost', port=5433, password='Inovepg123'):
        self.name = name
        self.host = host
        self.port = port
        self.password = password
        self.user = user
    
    def connect(self):
        self.conn = psycopg2.connect(database=self.name, user=self.user, password=self.password, host=self.host, port=self.port)
        return self.conn
    
    def close_db(self):
        self.conn.close()

    def get_cursor(self):
        conn = self.connect()
        self.cursor = conn.cursor()
        return self.cursor

    def list_products(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM produtos;")
        products = cursor.fetchall()

        if len(products) > 0:
            print('Listando produtos')
            print(100*'-')
            for product in products:
                print(f'ID:{product[0]} Nome:{product[1]} Preco:{product[2]} Estoque:{product[3]}')
                print(100*'-')
            self.close_db()
        else:
            print('Não existe produtos cadastrado no banco')
            self.close_db()

    def insert_product(self, nome, preco, estoque):
        cursor = self.get_cursor()
        try:
            cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque});")
            self.conn.commit()
            print('Produto cadastrado com successo')
            self.close_db()
        except Exception as e:
            print(f'Erro ao cadastrar produto: {e}')
            self.close_db()
       

    def update_product(self, id, nome, preco, estoque):
        cursor = self.get_cursor()
        try:
            cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={id}")
            print('Produto atualizado com sucesso')
            self.conn.commit()
            self.close_db()
        except Exception as e:
            print(f'ocorreu um erro ao atualizar produto:{e}')
            self.close_db()
        
    def delete_product(self, id):
        cursor = self.get_cursor()
        try:
            if not self.list_one_product(id):
                return False
            cursor.execute(f"DELETE FROM produtos WHERE id={id}")
            print('Produto delatado com sucesso')
            self.conn.commit()
            self.close_db()
        except Exception as e:
            print(f'ocorreu um erro ao deletar produto:{e}')
            self.close_db()
    
    def list_one_product(self, id):
        cursor = self.get_cursor()
        try:
            cursor.execute(f"SELECT * FROM produtos WHERE id={id}")
            produto = cursor.fetchone()
            if not produto:
                return print('produto não existe')
            print(f'Nome:{produto[1]}, preco:{produto[2]}, estoque:{produto[3]}')
            self.close_db()
        except Exception as e:
            print(f'erro ao buscar produto:{e}')

if __name__ == '__main__':
    crud = PostgreSqlOperations()   
    crud.delete_product(10)
