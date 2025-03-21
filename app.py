import logging
import pandas as pd
import re

from flask_cors import CORS 
from flask import Flask, jsonify, request
from lib.lib_db_manager import DBManager

app = Flask(__name__)

CORS(app)

db_manager = DBManager()  # Creating an instance of the DBManager class


def get_db_manager():
	global db_manager
	if db_manager is None:
		db_manager = DBManager()
	
	return db_manager


def hash_check(headers):
	status = None
	hash = headers.get('Authorization')
	if not hash or not get_db_manager().verify_hash(hash):
		status = jsonify({"error": "Invalid or missing hash."}), 401
	return status


@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()

	if not data or 'name' not in data or 'password' not in data:
		return jsonify({"error": "Name and password are required."}), 400

	name = data['name']
	password = data['password']

	hash = get_db_manager().verify_user_password(name, password)
	if hash:
		return jsonify({"hash": hash}), 200
	else:
		return jsonify({"error": "Invalid username or password."}), 401


@app.route('/post_anac_statistical', methods=['POST'])
def post_anac_statistical_data():
	try:
		status = hash_check(request.headers)
		if status is not None:
			return status

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
		status = hash_check(request.headers)
		if status is not None:
			return status

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
	status = hash_check(request.headers)
	if status is not None:
		return status

	mercado = request.args.get('mercado')
	ano_inicio = request.args.get('ano_inicio')
	mes_inicio = request.args.get('mes_inicio')
	ano_fim = request.args.get('ano_fim')
	mes_fim = request.args.get('mes_fim')
	limit = request.args.get('limit', default=10, type=int)
	page = request.args.get('page', default=1, type=int)

	# Validate market
	if not re.fullmatch(r'^[A-Za-z0-9]{8}$', mercado):
		return jsonify({"error": "Market must be a string with 8 alphanumeric characters."}), 400

	# Validate years
	if (not re.fullmatch(r'^\d{4}$', ano_inicio)) or (not re.fullmatch(r'^\d{4}$', ano_fim)):
		return jsonify({"error": "Years must be strings with four digits."}), 400

	# Validate months (accepting values from 1 to 12 with or without leading zero)
	if (not re.fullmatch(r'^(0?[1-9]|1[0-2])$', mes_inicio)) or (not re.fullmatch(r'^(0?[1-9]|1[0-2])$', mes_fim)):
		return jsonify({"error": "Months must be numbers between 1 and 12."}), 400

	# Validate date range
	if ano_inicio and ano_fim:
		if int(ano_fim) < int(ano_inicio):
			return jsonify({"error": "End year cannot be less than start year."}), 400
		if int(ano_fim) == int(ano_inicio) and mes_inicio and mes_fim and int(mes_fim) < int(mes_inicio):
			return jsonify({"error": "If start and end year are the same, end month cannot be less than start month."}), 400

	try:
		results, total_pages, current_page = get_db_manager().get_filtered_anac_range(
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