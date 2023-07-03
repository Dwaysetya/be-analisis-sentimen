from app import app
from flask import request
from models.dataset_model import database_model

obj = database_model()
@app.route('/dataset', methods=['GET'])
def get_dataset():
    return obj.get_dataset()
@app.route('/dataset/count', methods=['GET'])
def get_dataset_count():
    return obj.get_dataset_count()
@app.route('/dataset', methods=['POST'])
def import_dataset():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    obj.handle_dataset(file)
    return "Dataset successfully imported"
@app.route('/dataset/labelled', methods=['GET'])
def get_dataset_labelled():
    return obj.get_data_labelled()