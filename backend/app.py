import json
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
from cloud import upload_to_cloud_storage
from hume_embedding import getEmbeddingsLanguage
from clustering import run_clustering
from choose_query import choose_query_from_prompt
from utils import getCloudUrl, create_sentences, combine_date_and_time
from test_script import simulateSingleUploadCall
from db.pinecone.upload_content import embed_transcript_upload_pinecone
from db.pinecone.upload_emotion import upload_emotion_pinecone
from db.pinecone.query_content import query_pinecone_content
from db.pinecone.query_emotion import query_pinecone_emotion

from db.sql.models import db, Sentence
from db.sql.crud import create_sentence

# To run: flask run --host=0.0.0.0 --debug

app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db.init_app(app)

# # Create the database and the tables
# with app.app_context():
#   db.create_all()


@app.route("/")
def hello_world():
    return json.dumps("Hello World!!")


@app.route("/video", methods=["POST"])
def get_recording():
    (id, time, date) = upload_to_cloud_storage(request.data, 1)
    entryInfo = {
        "entry_id": id,
        "time": time,
        "date": date,
        "user_id": 0,
        "type": "video",
        "path": "local.mp4",
    }
    process_hume_results(entryInfo)
    return "Success"


@app.route("/audio", methods=["POST"])
def get_audio():
    (id, time, date) = upload_to_cloud_storage(request.data, 2)
    entryInfo = {
        "entry_id": id,
        "time": time,
        "date": date,
        "user_id": 0,
        "type": "audio",
        "path": "local.wav",
    }
    process_hume_results(entryInfo)
    return "Success"


@app.route("/text", methods=["POST"])
def get_text():
    (id, time, date) = upload_to_cloud_storage(request.data, 3)
    entryInfo = {
        "entry_id": id,
        "time": time,
        "date": date,
        "user_id": 0,
        "type": "audio",
        "path": "local.txt",
    }
    process_hume_results(entryInfo)
    return "Success"


# Given hume results, process them
""" 
JSON body input: {user_id, entry_id, type, date, time, path}

"""


# @app.route("/process_hume_results", methods=["POST"])
def process_hume_results(entryInfo):
    entry_data = simulateSingleUploadCall(entryInfo)
    ### 1: Process sentences, get openai embeddings and upload
    chunks_data = entry_data["chunks"]
    chunks = [chunk["text"] for chunk in chunks_data]

    chunks_df = pd.DataFrame(chunks_data)
    chunks_df["emotions"] = chunks_df["emotions"].apply(lambda x: np.array(x))
    chunks_df["index"] = chunks_df.index
    if "start_time" in chunks_df.columns and "end_time" in chunks_df.columns:
        chunks_df["duration"] = chunks_df["end_time"] - chunks_df["start_time"]
    else:
        # get number of words of text
        chunks_df["duration"] = chunks_df["text"].apply(lambda x: len(x.split(" ")))

    # Combines chunks (some are too short to be meaningful) into sentences of 20-30 words
    sentences = create_sentences(chunks_data, MIN_WORDS=20, MAX_WORDS=30)
    sentences_df = pd.DataFrame(sentences)

    # For each sentence in sentences_df, create an emotions column,
    # which is a weighted average of the emotions of the chunks that make up the sentence (start_chunk_id to end_chunk_id inclusive)
    # where the weights are the duration

    sentences_df["emotions"] = sentences_df.apply(
        lambda row: np.average(
            chunks_df.loc[row["start_chunk_id"] : row["end_chunk_id"]]["emotions"],
            weights=chunks_df.loc[row["start_chunk_id"] : row["end_chunk_id"]][
                "duration"
            ],
        ),
        axis=1,
    )

    sentences_df["emotions"] = sentences_df["emotions"].apply(lambda x: x.tolist())
    # Convert sentences to dictionary
    sentences_dict = sentences_df.to_dict(orient="records")

    date = entry_data["date"]
    time = entry_data["time"]
    timestamp = combine_date_and_time(date, time)

    ### sentences_dict: {sentence_num, text, sentence_length, start_chunk_id, end_chunk_id, emotions}
    for sentence in sentences_dict:
        create_sentence(
            user_id=entry_data["user_id"],
            entry_id=entry_data["entry_id"],
            sentence_id=sentence["sentence_num"],
            topic_id=None,
            video_link=None,
            timestamp=timestamp,
            start_time=sentence["start_time"],
            end_time=sentence["end_time"],
            transcript_text=sentence["text"],
            emotions=sentence["emotions"],
        )
        print("Created sentence: ", sentence["sentence_num"])

    # Embed transcript and upload to pinecone
    # sentences = [ sentence['text'] for sentence in sentences_dict ]
    # sentences_embeds = embed_transcript_upload_pinecone(sentences,
    #                                 user_id = entry_data['user_id'],
    #                                 entry_id = entry_data['entry_id'],
    #                                 upload = True)

    # # Upload emotional embeddings to pinecone
    # upload_emotion_pinecone(sentences_dict, user_id = entry_data['user_id'],
    #                         entry_id = entry_data['entry_id'],
    #                         upload = True)

    # # Clustering of sentences
    # episode_topics = run_clustering([sentences_dict], [sentences_embeds])

    # return {
    #   'sentences': sentences_dict,
    #   'episode_topics': episode_topics
    # }

    # Process emotions and metadata and upload to SQL - TODO
    # insertEmotion(sentences_dict, entryInfo)
    # return episode_topics


# Given a user query, determine which function to call
"""
JSON body input: {query: str, user_id: str}
"""


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json(force=True)
    query = data.get("query")
    user_id = 0

    print(query, user_id)

    # Run the query through the 'choose_query' function
    function_call = choose_query_from_prompt(query)
    if not function_call:
        print("No function call found")
        return

    function_name = function_call["name"]
    function_arguments = function_call["arguments"]

    if function_name == "make_sql_query":
        print("Function name sql query")
        return None
    elif function_name == "make_emotion_vector_db_query":
        print(f"Querying make_emotion_vector_db_query: {function_arguments}")
        emotion = function_arguments.get("emotion", None)
        # Embed emotion into an emotional vector (use Hume)
        emotion_emb = getEmbeddingFromString(emotion)
        print(f"Emotion embedding: {emotion_emb}")

        query_result = query_pinecone_emotion(emotion_emb, user_id, top_k=5)

        # Query pinecone for the top 5 closest emotional vectors
    elif function_name == "make_content_vector_db_query":
        topic = function_arguments.get("topic", None)
        start_time = function_arguments.get("start_time", None)
        end_time = function_arguments.get("end_time", None)

        query_result = query_pinecone_content(topic, user_id, top_k=5)
    # print("Query result", query_result)

    quotes = ""

    for result in query_result:
        quotes += '"' + (result["text"]) + '"\n\n'

    return json.dumps(quotes)


def getEmbeddingFromString(query):
    # Convert the string into a file
    filename = "temp.txt"
    with open(filename, "w") as f:
        f.write(query)
    # Get the embeddings
    absolute_path = str(Path(filename).resolve())
    embedding = getEmbeddingsLanguage(absolute_path)
    return embedding[0]["emotions"]


@app.route("/query_db")
def index():
    # Querying the database
    sentences = Sentence.query.all()
    return sentences


if __name__ == "__main__":
    app.run()
