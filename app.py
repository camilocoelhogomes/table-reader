from flask import Flask, jsonify, make_response, send_file, request
from flask_cors import CORS, cross_origin
import base64
from textract import *

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/alive', methods=['GET'])
@cross_origin(supports_credentials=True)
def isAlive():
    return make_response(jsonify(message='estou vivo'))


@app.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def hello_from_root():
    body = request.get_json()['img']
    base64_img = body[(body.find(',')+1):]
    imgdata = base64.b64decode(base64_img)
    output = extract(imgdata)
    with open("/tmp/csv_file.csv", "w+") as fout:
        fout.write(output)
    return send_file("/tmp/csv_file.csv", as_attachment=True, mimetype="text/csv")


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
