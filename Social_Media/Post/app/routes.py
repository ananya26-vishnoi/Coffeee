from flask import Blueprint, request
from dotenv import load_dotenv
from .models import Post, User
load_dotenv()
posts_blueprint = Blueprint('post', __name__)


@posts_blueprint.route("/create", methods=['POST'])
def create_post():
  # Post has -> id, title, content, authors, created_date, updated_date
  # Getting data from frontend
    data = request.get_json()
    if "title" not in data or "content" not in data or "user_token" not in data:
        return {"message":"Title, Content, User Token is required"}, 400
    
    user_token = data["user_token"]

    # Check if user is logged in
    user = User().verify_user(data["user_token"])
    print(user)
    if user is None:
        return {"mesage":"User not found"}, 400
    
    # Get user id from response
    user_id = user['user_id']

    # Create post
    url = Post().create_post(data["title"], data["content"], user_id)
    ret_Data = {
        "url": url,
        "message": "Post created",
        "title" : data["title"],
        "content" : data["content"],
    }
    return ret_Data, 200
    
@posts_blueprint.route("/share", methods=['GET'])
def get_post():
    # get url from get request
    data = request.args
    if "url" not in data:
        return {"message":"URL is required"}, 400
    url = data["url"]

    # Get post from database
    post = Post().get_post(url)

    # Check if post exists
    if post is None:
        return {"message":"Post not found"}, 404
    
    # Get user from user service
    return post, 200

@posts_blueprint.route("/getAll", methods=['GET'])
def get_all_posts():
    user_id = request.args.get("user_id")
    posts = Post().get_all_posts(user_id)
    if posts is None:
        return {"message":"No posts found"}, 200
    return posts, 200
