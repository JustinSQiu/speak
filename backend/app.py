import json
from flask import Flask, request
from flask_cors import CORS

from google.cloud import storage

import sqlite3
import uuid
from datetime import datetime

client = storage.Client.from_service_account_json('./calhacks-390202-77187dbaceae.json')
bucket = client.get_bucket('calhacks-videos')

def insert_entry(id, time, date, conn, cursor):
    insert_query = "INSERT INTO entries (id, time, date) VALUES (?, ?, ?);"
    cursor.execute(insert_query, (id, time, date))
    conn.commit()

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

    new_id = str(uuid.uuid4())  # Generate a UUID
    current_time = datetime.now().strftime('%H:%M:%S')  # Get current time
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get current date

    conn = sqlite3.connect('memos.db') 
    cursor = conn.cursor()

    insert_entry(new_id, current_time, current_date, conn, cursor)

    blob_name = f"{new_id}.mp4" 
    blob = bucket.blob(blob_name)
    blob.content_type = 'video/mp4'
    blob.upload_from_filename(file_path)
    conn.close()
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

    new_id = str(uuid.uuid4())  # Generate a UUID
    current_time = datetime.now().strftime('%H:%M:%S')  # Get current time
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get current date

    conn = sqlite3.connect('memos.db') 
    cursor = conn.cursor()

    insert_entry(new_id, current_time, current_date, conn, cursor)

    blob_name = f"{new_id}.wav" 
    blob = bucket.blob(blob_name)
    blob.content_type = 'audio/wav'
    blob.upload_from_filename(file_path)
    conn.close()
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

    new_id = str(uuid.uuid4())  # Generate a UUID
    current_time = datetime.now().strftime('%H:%M:%S')  # Get current time
    current_date = datetime.now().strftime('%Y-%m-%d')  # Get current date

    conn = sqlite3.connect('memos.db') 
    cursor = conn.cursor()

    insert_entry(new_id, current_time, current_date, conn, cursor)

    blob_name = f"{new_id}.txt" 
    blob = bucket.blob(blob_name)
    blob.content_type = 'text/plain'
    blob.upload_from_filename(file_path)
    conn.close()
    return "Success"
