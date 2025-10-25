from flask import Flask, jsonify, request
from db import get_users, add_user

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask App on Kubernetes with PostgreSQL"})

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({"error": "name is required"}), 400
        add_user(name)
        return jsonify({"message": f"user '{name}' created"}), 201
    else:
        users = get_users()
        return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
