import logging
import pandas as pd

from flask import Flask, jsonify, request
from lib.lib_db_manager import DBManager

app = Flask(__name__)
db_manager = DBManager()  # Creating an instance of the DBManager class

def get_db_manager():
	global db_manager
	if db_manager is None:
		db_manager = DBManager()
	
	return db_manager

@app.route('/')
def home():
	return "Hello World!"

@app.route('/users', methods=['GET'])
def get_users():
	users = get_db_manager().get_all_users()
	return jsonify(users)

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

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)