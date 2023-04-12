import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request
from aifw import DetectorMiddleware

app = Flask(__name__)
app.wsgi_app = DetectorMiddleware(app.wsgi_app)

METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/', methods=['GET'])
def index():
    ## Vulnerable to XSS!!!
    return {
		"path": request.path,
		"args": request.args,
		"method": request.method,
	}

@app.route('/data', methods=['POST', 'PUT'])
def data():
    ## Vulnerable to XSS!!!
    return {
        "path": request.path,
		"args": request.args,
		"method": request.method,
        "data": request.get_data(as_text=True)[:0xff]
    }