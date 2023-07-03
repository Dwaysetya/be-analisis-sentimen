from app import app
from flask import request, jsonify
from models.preprocessing_model import preprocessing_model

obj = preprocessing_model()
@app.route('/preprocessing', methods=['GET'])
def do_preprocessing():
    preprocessed_data = obj.preprocessing()
    return preprocessed_data