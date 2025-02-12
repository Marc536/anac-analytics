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

	# Example of function to get data
	def get_all_table_anac(self):
		conn = self.get_connection()
		cur = conn.cursor()
		cur.execute('SELECT * FROM anac;')
		users = cur.fetchall()
		cur.close()
		return users

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
			"ano",
			"mes",
			-- Concatenate aeroporto_de_origem_nome and aeroporto_de_destino_nome in alphabetical order
			LEAST("aeroporto_de_origem_nome", "aeroporto_de_destino_nome") || ' - ' ||
			GREATEST("aeroporto_de_origem_nome", "aeroporto_de_destino_nome") AS "mercado",
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

	# Close the connection
	def close_connection(self):
		if self.conn:
			self.conn.close()
			self.conn = None

