from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from controllers import *
from controllers.stopword_controller import *
from controllers.slangword_controller import *
