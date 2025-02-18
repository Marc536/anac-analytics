import psycopg2
from psycopg2 import sql
import os
import io

class DBManager:
	def __init__(self):
		self.conn = None

	# Database connection
	def get_connection(self):
		if not self.conn:
			self.conn = psycopg2.connect(
				host=os.getenv('DB_HOST'),
				database=os.getenv('DB_NAME'),
				user=os.getenv('DB_USER'),
				password=os.getenv('DB_PASSWORD')
			)
		return self.conn

	def post_table_anac(self, df):
		conn = self.get_connection()
		cur = conn.cursor()

		# Quickly delete all records and reset ID
		cur.execute("TRUNCATE TABLE anac RESTART IDENTITY;")

		colunas_csv = df.columns.str.lower().tolist()

		# Create CSV buffer in memory
		csv_buffer = io.StringIO()
		df.to_csv(csv_buffer, index=False, header=False, sep=";", na_rep="NULL")
		csv_buffer.seek(0)

		# Save data in the database
		cur.copy_from(csv_buffer, "anac", sep=";", null="NULL", columns=colunas_csv)

		conn.commit()
		cur.close()

	def post_table_anac_filtered(self):
		conn = self.get_connection()
		cur = conn.cursor()

		# Check if the 'anac' table exists
		cur.execute("""
		SELECT to_regclass('public.anac');
		""")
		table_exists = cur.fetchone()[0]

		if table_exists is None:
			# Return -1 if the table doesn't exist
			cur.close()
			return -1

		# Drop the table if it exists
		cur.execute("DROP TABLE IF EXISTS anac_filtered;")
		
		# Create the new filtered table based on conditions with correct columns
		create_table_sql = """
		CREATE TABLE anac_filtered AS
		SELECT 
			CAST("ano" AS INTEGER) AS "ano",  -- Casting "ano" to INTEGER
			CAST("mes" AS INTEGER) AS "mes",  -- Casting "mes" to INTEGER
			-- Concatenate aeroporto_de_origem_sigla and aeroporto_de_destino_sigla in alphabetical order
			LEAST("aeroporto_de_origem_sigla", "aeroporto_de_destino_sigla") ||
			GREATEST("aeroporto_de_origem_sigla", "aeroporto_de_destino_sigla") AS "mercado",
			"rpk"
		FROM anac
		WHERE "empresa_sigla" = 'GLO'
		AND "natureza" = 'DOMÉSTICA'
		AND "grupo_de_voo" = 'REGULAR';
		"""
		cur.execute(create_table_sql)
		
		# Commit and close cursor
		conn.commit()
		cur.close()

	def get_filtered_anac_range(self, ano_inicio=None, mes_inicio=None, ano_fim=None, mes_fim=None, mercado=None, limit=10, page=1):
		conn = self.get_connection()
		cur = conn.cursor()
		
		# Building the query with dynamic filters
		query = "SELECT ano, mes, mercado, rpk FROM anac_filtered WHERE 1=1"
		params = []
		
		if ano_inicio and mes_inicio and ano_fim and mes_fim:
			query += " AND (ano, mes) BETWEEN (%s, %s) AND (%s, %s)"
			params.extend([ano_inicio, mes_inicio, ano_fim, mes_fim])
		
		if mercado:
			query += " AND mercado = %s"
			params.append(mercado)
		
		# Total record count
		count_query = f"SELECT COUNT(*) FROM ({query}) AS count_query"
		cur.execute(count_query, params)
		total_records = cur.fetchone()[0]
		
		# Calculation of the total number of pages
		total_pages = (total_records // limit) + (1 if total_records % limit > 0 else 0)
		
		# Adds pagination
		offset = (page - 1) * limit
		query += " ORDER BY ano, mes LIMIT %s OFFSET %s"
		params.extend([limit, offset])
		
		cur.execute(query, params)
		results = cur.fetchall()
		
		cur.close()
		
		return results, total_pages, page


	def verify_user_password(self, name, password):
		conn = self.get_connection()
		cur = conn.cursor()
		
		query = "SELECT password, hash FROM users WHERE name = %s"
		cur.execute(query, (name,))
		
		result = cur.fetchone()
		
		if result is None:
			cur.close()
			return False
		
		stored_password, stored_hash = result
		
		if password == stored_password:
			cur.close()
			return stored_hash
		else:
			cur.close()
			return False


	def verify_hash(self, hash):
		conn = self.get_connection()
		cur = conn.cursor()
		
		query = "SELECT hash FROM users WHERE hash = %s"
		cur.execute(query, (hash,))
		
		result = cur.fetchone()
		
		if result is None:
			cur.close()
			return False
		
		cur.close()
		return True


	# Close the connection
	def close_connection(self):
		if self.conn:
			self.conn.close()
			self.conn = None

