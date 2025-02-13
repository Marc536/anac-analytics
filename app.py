import logging
import pandas as pd
import re

from flask import Flask, jsonify, request
from lib.lib_db_manager import DBManager

app = Flask(__name__)
db_manager = DBManager()  # Creating an instance of the DBManager class


def get_db_manager():
	global db_manager
	if db_manager is None:
		db_manager = DBManager()
	
	return db_manager


@app.route('/post_anac_statistical', methods=['POST'])
def post_anac_statistical_data():
	try:
		file = request.files['file']
		df = pd.read_csv(file.stream, delimiter=';', skiprows=1)
		get_db_manager().post_table_anac(df)
		return jsonify({"message": "CSV uploaded and saved to PostgreSQL successfully!"}), 201
	except Exception as e:
		logging.error(f"{e}")
		return jsonify({"message": "Error uploading the CSV file. \
			Please check if the file is in the correct format and try again."
		}), 400


@app.route('/post_table_anac_filtered', methods=['POST'])
def post_table_anac_filtered():
	try:
		status = get_db_manager().post_table_anac_filtered()
		if status == -1:
			return jsonify({"message": "data not found!"}), 404
		return jsonify({"message": "CSV uploaded and saved to PostgreSQL successfully!"}), 201
	except Exception as e:
		logging.error(f"{e}")
		return jsonify({"message": "Error uploading the CSV file. \
			Please check if the file is in the correct format and try again."
		}), 400


@app.route('/get_table_anac_filtered', methods=['GET'])
def get_table_anac_filtered():
	mercado = request.args.get('mercado')
	ano_inicio = request.args.get('ano_inicio')
	mes_inicio = request.args.get('mes_inicio')
	ano_fim = request.args.get('ano_fim')
	mes_fim = request.args.get('mes_fim')
	limit = request.args.get('limit', default=10, type=int)
	page = request.args.get('page', default=1, type=int)

	# Validate market
	if mercado and not re.fullmatch(r'^[A-Za-z0-9]{8}$', mercado):
		return jsonify({"error": "Market must be a string with 8 alphanumeric characters."}), 400

	# Validate years
	if (ano_inicio and not re.fullmatch(r'^\d{4}$', ano_inicio)) or (ano_fim and not re.fullmatch(r'^\d{4}$', ano_fim)):
		return jsonify({"error": "Years must be strings with four digits."}), 400

	# Validate months (accepting values from 1 to 12 with or without leading zero)
	if (mes_inicio and not re.fullmatch(r'^(0?[1-9]|1[0-2])$', mes_inicio)) or (mes_fim and not re.fullmatch(r'^(0?[1-9]|1[0-2])$', mes_fim)):
		return jsonify({"error": "Months must be numbers between 1 and 12."}), 400

	# Validate date range
	if ano_inicio and ano_fim:
		if int(ano_fim) < int(ano_inicio):
			return jsonify({"error": "End year cannot be less than start year."}), 400
		if int(ano_fim) == int(ano_inicio) and mes_inicio and mes_fim and int(mes_fim) < int(mes_inicio):
			return jsonify({"error": "If start and end year are the same, end month cannot be less than start month."}), 400

	try:
		results, total_pages, current_page = db_manager.get_filtered_anac_range(
			ano_inicio, 
			mes_inicio, 
			ano_fim, 
			mes_fim, 
			mercado, 
			limit, 
			page
		)
	except Exception as e:
		logging.error(f"{e}")
		return jsonify({"message": "error searching database"}), 400


	return jsonify({
		"data": results,
		"total_pages": total_pages,
		"current_page": current_page
	}), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)