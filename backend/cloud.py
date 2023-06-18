import sqlite3
import uuid
from datetime import datetime

from google.cloud import storage

VIDEO, AUDIO, TEXT = 1, 2, 3

client = storage.Client.from_service_account_json("./calhacks-390202-77187dbaceae.json")
bucket = client.get_bucket("calhacks-videos")


def insert_entry(id, time, date, type, conn, cursor):
    insert_query = "INSERT INTO entries (id, time, date, type) VALUES (?, ?, ?, ?);"
    cursor.execute(insert_query, (id, time, date, type))
    conn.commit()


def upload_to_cloud_storage(data, type):
    new_id = str(uuid.uuid4())  # Generate a UUID
    current_time = datetime.now().strftime("%H:%M:%S")  # Get current time
    current_date = datetime.now().strftime("%Y-%m-%d")  # Get current date

    if type == VIDEO:
        file_path = "./local.mp4"
        blob_name = f"{new_id}.mp4"
        c_type = "video/mp4"
    elif type == AUDIO:
        file_path = "./local.wav"
        blob_name = f"{new_id}.wav"
        c_type = "audio/wav"
    elif type == TEXT:
        file_path = "./local.txt"
        blob_name = f"{new_id}.txt"
        c_type = "text/plain"

    with open(file_path, "wb") as destination:
        contents = data
        destination.write(contents)

    conn = sqlite3.connect("memos.db")
    cursor = conn.cursor()

    insert_entry(new_id, current_time, current_date, c_type, conn, cursor)

    blob = bucket.blob(blob_name)
    blob.content_type = c_type
    blob.upload_from_filename(file_path)
    blob.download_to_filename(file_path)
    conn.close()
    return new_id, current_time, current_date


def regenerateDB():
    conn = sqlite3.connect("memos.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS entries;")
    cursor.execute(
        """CREATE TABLE entries (
            id text PRIMARY KEY,
            time text NOT NULL,
            date text NOT NULL,
            type text NOT NULL
        );"""
    )
    conn.commit()
    conn.close()
