import json
from flask import Flask, request
from flask_cors import CORS
from cloud import upload_to_cloud_storage
from hume_embeding import getEmbeddingsLanguage
from utils import getCloudUrl

# To run: flask run --host=0.0.0.0 --debug

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return json.dumps("Hello World!!")


@app.route("/video", methods=["POST"])
def get_recording():
    (id, time, date) = upload_to_cloud_storage(request.data, 1)
    url = getCloudUrl(id)
    processedEmbeddings = getEmbeddingsLanguage(url)
    metadata = {
        "journalId": id,
        "time": time,
        "date": date,
        "userId": 0,
        "type": "video",
    }
    return "Success"


@app.route("/audio", methods=["POST"])
def get_audio():
    (id, time, date) = upload_to_cloud_storage(request.data, 2)
    return "Success"


@app.route("/text", methods=["POST"])
def get_text():
    (id, time, date) = upload_to_cloud_storage(request.data, 3)
    return "Sucess"
