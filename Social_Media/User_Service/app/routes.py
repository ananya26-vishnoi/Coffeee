# app/routes.py

from flask import jsonify, request
from app import app
from app.models import User
from flask_bcrypt import Bcrypt
import jwt
from functools import wraps
from app import mongo

bcrypt = Bcrypt()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.find_by_username(data['username'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

    if User.find_by_username(username):
        return jsonify({'message': 'Username already exists!'}), 400

    if User.find_by_email(email):
        return jsonify({'message': 'Email already exists!'}), 400

    new_user = User(username, email, password)
    new_user.save()

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Invalid credentials!'}), 401

    user = User.find_by_username(auth.username)

    if not user or not bcrypt.check_password_hash(user['password'], auth.password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({'username': user['username']}, app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')}), 200

@app.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    return jsonify({
        'username': current_user['username'],
        'email': current_user['email']
    }), 200
