from flask import Blueprint, request
import requests
from dotenv import load_dotenv
from .models import User
load_dotenv()
import os
users_blueprint = Blueprint('user', __name__)


@users_blueprint.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    if "first_name" not in data or "last_name" not in data or "email" not in data or "password" not in data:
        return {"message":"Email, Password, First name, last name also required is required"}, 400
    
    user = User().create_user(data["email"], data["password"], data["first_name"], data["last_name"])

    if user is None:
        return {"mesage":"User already exists"}, 400
    
    ret_data = {
        "message" : "User created",
        "user_token": user,
        "email" : data["email"],
        "first_name" : data["first_name"],
        "last_name" : data["last_name"]
    }
    return ret_data, 200

@users_blueprint.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    if "email" not in data or "password" not in data:
        return {"message":"Email, Password is required"}, 400
    
    user = User().login(data["email"], data["password"])

    if user is None:
        return {"mesage":"Incorrect email or password"}, 400
    
    ret_data = {
        "message" : "User logged in",
        "user_token": user,
        "email" : data["email"]
    }
    return ret_data, 200

@users_blueprint.route("/verify", methods=['POST'])
def verify():
    data = request.get_json()
    if "user_token" not in data:
        return {"message":"User Token is required"}, 400
    
    user = User().verify_user(data["user_token"])
    print(user)
    if user is None:
        return {"mesage":"User not found"}, 400
    
    ret_data = {
        "message" : "User logged in",
        "user": user
    }
    return ret_data, 200
