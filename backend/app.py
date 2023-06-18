import json
from flask import Flask, request
from flask_cors import CORS

from google.cloud import storage

client = storage.Client.from_service_account_json('./calhacks-390202-77187dbaceae.json')
bucket = client.get_bucket('calhacks-videos')

# To run: flask run --host=0.0.0.0 --debug

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return json.dumps("Hello World!!")

@app.route("/video",  methods=['POST'])
def get_recording():
    data = request.data
    file_path = './local.mp4'
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        return "Failure"

    blob_name = 'video.mp4' 
    blob = bucket.blob(blob_name)
    blob.content_type = 'video/mp4'
    blob.upload_from_filename(file_path)
    return "Success"

@app.route("/audio", methods=["POST"])
def get_audio():
    data = request.data
    file_path = './local.wav'
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        return "Failure"

    blob_name = 'audio.wav' 
    blob = bucket.blob(blob_name)
    blob.content_type = 'audio/wav'
    blob.upload_from_filename(file_path)
    return "Success"

@app.route('/text', methods=["POST"])
def get_text():
    data = request.data
    file_path = './local.txt'
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
    except Exception as e:
        return "Failure"

    blob_name = 'text.txt' 
    blob = bucket.blob(blob_name)
    blob.content_type = 'text/plain'
    blob.upload_from_filename(file_path)
    return "Success"
