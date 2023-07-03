from app import app
from flask import request
from models.stopword_model import stopword_model

obj = stopword_model()
@app.route('/stopword', methods=['GET'])
def getall_stopword():
    return obj.getall_stopword()

@app.route('/stopword/import', methods=['POST'])
def import_stopword():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    obj.import_stopwords(file)
    return "Stopwords successfully imported"

@app.route('/stopword/limit/<limit>/page/<page>', methods=['GET'])
def stopword_pagination(limit, page):
    return obj.stopword_pagination(limit, page)

@app.route('/stopword', methods=['POST'])
def add_stopword():
    data = request.get_json()
    return obj.add_stopword(data)

@app.route('/stopword/update/<id>', methods=['PUT'])
def update_stopword(id):
    data = request.get_json()
    return obj.update_stopword(id, data)

@app.route('/stopword/delete/<id>', methods=['DELETE'])
def delete_stopword(id):
    return obj.delete_stopword(id)