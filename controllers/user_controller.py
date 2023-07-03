from app import app
from flask import request, send_file
from models.user_model import user_model
import json

obj = user_model()
@app.route('/user/getall', methods=['GET'])
def getall():
    return obj.user_get_all()

@app.route('/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return obj.user_sign_up(data)

@app.route('/user/signin', methods=['POST'])
def signin():
    data = request.get_json()
    return obj.user_sign_in(data)

@app.route('/user/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    return obj.user_update(user_id, data)

@app.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return obj.user_delete(user_id)

@app.route('/user/getall/limit/<limit>/page/<page>', methods=['GET'])
def user_pagination(limit, page):
    return obj.user_pagination(limit, page)

# @app.route('/upload_csv', methods=['POST'])
# def upload_csv():
#     data = request.files
#     return dataset.import_dataset(data)