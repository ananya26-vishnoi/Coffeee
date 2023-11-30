from flask import Blueprint, request
import requests
from dotenv import load_dotenv
from .models import Social
load_dotenv()
import os
social_blueprint = Blueprint('post', __name__)


@social_blueprint.route("/follow", methods=['POST'])
def follow():
    data = request.get_json()
    if "user_1" not in data or "user_2" not in data:
        return {"message":"User 1, and User 2 is required"}, 400
    
    user_1 = data["user_1"]
    user_2 = data["user_2"]

    if user_1 == user_2:    
        return {"message":"User 1 and User 2 cannot be the same"}, 400
    
    ret = Social().create_interaction(user_1,user_2,"Following")
    if ret == "not_exists":
        return {"message":"Either of 1 user does not exists"}, 400

    if ret == "already_exists":
        return {"message":"User 1 already follows User 2"}, 400
    
    return {"message":"User 1 is now following User 2"}, 200

@social_blueprint.route("/like", methods=['POST'])
def like():
    # checking if got all data from frontend
    data = request.get_json()
    if "user_1" not in data or "user_2" not in data or "post_id" not in data:
        return {"message":"User 1, and User 2 is required"}, 400
    
    # getting data from frontend
    user_1 = data["user_1"]
    user_2 = data["user_2"]
    post_id = data["post_id"]

    # Incase user are same
    if user_1 == user_2:    
        return {"message":"User 1 and User 2 cannot be the same"}, 400
    
    # Creating Interaction
    ret = Social().create_interaction(user_1,user_2,"Like",post_id=post_id)

    # Checking if user exists
    if ret == "not_exists":
        return {"message":"Either of 1 user does not exists"}, 400
    
    # Checking if interaction already exists
    if ret == "already_exists":
        return {"message":"User 1 has already liked User 2's post"}, 400

    # Checking if post exists
    if ret == "post_not_exists":
        return {"message":"Post does not exists"}, 400
    
    return {"message":"User 1 has liked User 2's post"}, 200

@social_blueprint.route("/comment", methods=['POST'])
def comment():
    data = request.get_json()
    if "user_1" not in data or "user_2" not in data or "text" not in data or "post_id" not in data:
        return {"message":"User 1, User 2, and Text is required"}, 400
    
    user_1 = data["user_1"]
    user_2 = data["user_2"]
    text = data["text"]
    post_id = data["post_id"]

    if user_1 == user_2:    
        return {"message":"User 1 and User 2 cannot be the same"}, 400
    
    ret = Social().create_interaction(user_1,user_2,"Comment",text,post_id=post_id)

    if ret == "not_exists":
        return {"message":"Either of 1 user does not exists"}, 400

    if ret == "already_exists":
        return {"message":"User 1 already commented on User 2's post"}, 400
    
    # Checking if post exists
    if ret == "post_not_exists":
        return {"message":"Post does not exists"}, 400
    
    return {"message":"User 1 has commented on User 2's post"}, 200

@social_blueprint.route("/view_posts", methods=['GET'])
def view_posts():
    user_1 = request.args.get("user_1")
    user_2 = request.args.get("user_2")

    if user_1 is None or user_2 is None:
        return {"message":"User 1 and User 2 is required"}, 400

    if user_1 == user_2:
        return {"message":"User 1 and User 2 cannot be the same"}, 400
    
    # check if user 1 follows user 2
    follows = Social().check_follow(user_1,user_2)
    if not follows:
        return {"message":"User 1 does not follow User 2"}, 400
    
    # Get all posts from user_2
    url = "http://localhost:"+os.environ.get("POST_APP_PORT") + "/post/getAll?user_id="+str(user_2)
    response = requests.get(url)
    if response.status_code != 200:
        return {"message":"Error getting posts"}, 400
    
    return response.json(), 200

@social_blueprint.route("/check_follow", methods=['POST'])
def check_follow():
    data = request.get_json()
    if "user_1" not in data or "user_2" not in data:
        return {"message":"User 1 and User 2 is required"}, 400
    
    user_1 = data["user_1"]
    user_2 = data["user_2"]

    if user_1 == user_2:
        return {"message":"User 1 and User 2 cannot be the same"}, 400
    
    # check if user 1 follows user 2
    follows = Social().check_follow(user_1,user_2)
    if not follows:
        return {"message":"User 1 does not follow User 2","status" : False}, 400
    
    return {"message":"User 1 follows User 2","status" : True}, 200