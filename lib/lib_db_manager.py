import psycopg2
from psycopg2 import sql
import os

class DBManager:
	def __init__(self):
		self.conn = None

	# Conexão com o banco de dados
	def get_connection(self):
		if not self.conn:
			self.conn = psycopg2.connect(
				host=os.getenv('DB_HOST'),
				database=os.getenv('DB_NAME'),
				user=os.getenv('DB_USER'),
				password=os.getenv('DB_PASSWORD')
			)
		return self.conn

	# Exemplo de função para obter dados
	def get_all_users(self):
		conn = self.get_connection()
		cur = conn.cursor()
		cur.execute('SELECT * FROM anac;')  # Supondo que você tenha uma tabela 'users'
		users = cur.fetchall()
		cur.close()
		return users

	def post_table_anac(self, df):
		conn = self.get_connection()
		cur = conn.cursor()

		# Remove todos os registros antes de inserir novos dados
		cur.execute("DELETE FROM anac;")

		# Obtém os nomes das colunas do DataFrame (após o descarte da primeira linha)
		columns = df.columns.tolist()

		# Prepara os dados em um formato de lista para inserção em massa
		data = [tuple(row) for _, row in df.iterrows()]

		# Cria a string de colunas dinamicamente
		col_str = ", ".join(columns)
		placeholders = ", ".join(["%s"] * len(columns))  # Gerar o mesmo número de placeholders (%s) para cada coluna

		# Inserção em massa usando executemany
		cur.executemany(f'''
			INSERT INTO anac ({col_str})
			VALUES ({placeholders})
		''', data)

		conn.commit()
		cur.close()

	# Fechar a conexão
	def close_connection(self):
		if self.conn:
			self.conn.close()
			self.conn = None

