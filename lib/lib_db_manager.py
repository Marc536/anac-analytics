import psycopg2
from psycopg2 import sql
import os
import io

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

		# Apagar todos os registros rapidamente e resetar ID
		cur.execute("TRUNCATE TABLE anac RESTART IDENTITY;")

		colunas_csv = df.columns.str.lower().tolist()

		# Criar buffer CSV na memória
		csv_buffer = io.StringIO()
		df.to_csv(csv_buffer, index=False, header=False, sep=";", na_rep="NULL")  # Sem 'quotechar'
		csv_buffer.seek(0)

		# Executar COPY
		cur.copy_from(csv_buffer, "anac", sep=";", null="NULL", columns=colunas_csv)

		conn.commit()
		cur.close()

	# Fechar a conexão
	def close_connection(self):
		if self.conn:
			self.conn.close()
			self.conn = None

