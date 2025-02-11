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
				host=os.getenv('DB_HOST', 'postgres'),
				database=os.getenv('DB_NAME', 'ANAC'),
				user=os.getenv('DB_USER', 'postgres'),
				password=os.getenv('DB_PASSWORD', '1234')
			)
		return self.conn

	# Exemplo de função para obter dados
	def get_all_users(self):
		conn = self.get_connection()
		cur = conn.cursor()
		cur.execute('SELECT * FROM users;')  # Supondo que você tenha uma tabela 'users'
		users = cur.fetchall()
		cur.close()
		return users

	# Função para inserir dados (exemplo)
	def create_user(self, name, email):
		conn = self.get_connection()
		cur = conn.cursor()
		cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
		conn.commit()
		cur.close()

	# Fechar a conexão
	def close_connection(self):
		if self.conn:
			self.conn.close()
			self.conn = None

