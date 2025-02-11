from flask import Flask, jsonify, request
from lib.lib_db_manager import DBManager

app = Flask(__name__)
db_manager = DBManager()  # Criando uma instância da classe DBManager

@app.route('/')
def home():
	return "Hello World!"

@app.route('/users', methods=['GET'])
def get_users():
	users = db_manager.get_all_users()  # Usando o método para obter todos os usuários
	return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
	name = request.json.get('name')
	email = request.json.get('email')
	db_manager.create_user(name, email)  # Usando o método para criar um usuário
	return jsonify({"message": "User created successfully!"}), 201

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)