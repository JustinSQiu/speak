import json
from flask import Flask, request
from flask_cors import CORS
from cloud import upload_to_cloud_storage

# To run: flask run --host=0.0.0.0 --debug

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return json.dumps("Hello World!!")

@app.route("/video",  methods=['POST'])
def get_recording():
    upload_to_cloud_storage(request.data, 1)
    return "Success"


@app.route("/audio", methods=["POST"])
def get_audio():
    upload_to_cloud_storage(request.data, 2)
    return "Success"

@app.route('/text', methods=["POST"])
def get_text():
    upload_to_cloud_storage(request.data, 3)
    return "Sucess"
