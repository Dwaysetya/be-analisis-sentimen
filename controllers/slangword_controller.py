from app import app
from flask import request
from models.slangword_model import slangword_model

obj = slangword_model()
@app.route('/slangword', methods=['GET'])
def getall_slangword():
    return obj.getall_slangword()

@app.route('/slangword/import', methods=['POST'])
def import_slangword():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    obj.import_slangwords(file)
    return "Slangwords successfully imported"

@app.route('/slangword/limit/<limit>/page/<page>', methods=['GET'])
def slangword_pagination(limit, page):
    return obj.slangword_pagination(limit, page)

@app.route('/slangword', methods=['POST'])
def add_slangword():
    data = request.get_json()
    return obj.add_slangword(data)

@app.route('/slangword/update/<id>', methods=['PUT'])
def update_slangword(id):
    data = request.get_json()
    return obj.update_slangword(id, data)

@app.route('/slangword/delete/<id>', methods=['DELETE'])
def delete_slangword(id):
    return obj.delete_slangword(id)