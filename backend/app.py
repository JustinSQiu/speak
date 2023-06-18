import json
from flask import Flask, request
from flask_cors import CORS

import pandas as pd
import numpy as np
from cloud import upload_to_cloud_storage
from hume_embedding import getEmbeddingsLanguage
from clustering import run_clustering
from choose_query import choose_query_from_prompt
from utils import getCloudUrl, create_sentences
from test_script import simulateSingleUploadCall
from db.pinecone.upload_content import embed_transcript_upload_pinecone
from db.pinecone.query_content import query_pinecone

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
    return "Success"


# Given hume results, process them
''' 
JSON body input: {user_id, entry_id, type, date, time, path}

'''
@app.route('/process_hume_results', methods=['POST'])
def process_hume_results():
  entryInfo = request.get_json()
  entry_data = simulateSingleUploadCall(entryInfo)
  
  ### 1: Process sentences, get openai embeddings and upload
  chunks_data = entry_data['chunks']
  chunks = [ chunk['text'] for chunk in chunks_data ]

  chunks_df = pd.DataFrame(chunks_data)
  chunks_df['emotions'] = chunks_df['emotions'].apply(lambda x: np.array(x))
  chunks_df['index'] = chunks_df.index
  if 'start_time' in chunks_df.columns and 'end_time' in chunks_df.columns:
      chunks_df['duration'] = chunks_df['end_time'] - chunks_df['start_time']
  else:
      # get number of words of text
      chunks_df['duration'] = chunks_df['text'].apply(lambda x: len(x.split(' ')))

  # Combines chunks (some are too short to be meaningful) into sentences of 20-30 words
  sentences = create_sentences(chunks, MIN_WORDS=20, MAX_WORDS=30)
  sentences_df = pd.DataFrame(sentences)

  # For each sentence in sentences_df, create an emotions column, 
  # which is a weighted average of the emotions of the chunks that make up the sentence (start_chunk_id to end_chunk_id inclusive)
  # where the weights are the duration

  sentences_df['emotions'] = sentences_df.apply( lambda row: np.average(chunks_df.loc[row['start_chunk_id']:row['end_chunk_id']]['emotions'],
                                                                          weights=chunks_df.loc[row['start_chunk_id']:row['end_chunk_id']]['duration']), axis=1)
      
  sentences_df['emotions'] = sentences_df['emotions'].apply(lambda x: x.tolist())   
  # Convert sentences to dictionary
  sentences_dict = sentences_df.to_dict(orient='records')
  
  ### sentences_dict: {sentence_num, text, sentence_length, start_chunk_id, end_chunk_id}
  
  # Embed transcript and upload to pinecone
  sentences = [ sentence['text'] for sentence in sentences_dict ]
  sentences_embeds = embed_transcript_upload_pinecone(sentences, 
                                  user_id = entry_data['user_id'],
                                  entry_id = entry_data['entry_id'])
  
  # Clustering of sentences
  episode_topics = run_clustering([sentences_dict], [sentences_embeds])
  
  # Process emotions and metadata and upload to SQL - TODO

  return episode_topics


# Given a user query, determine which function to call
'''
JSON body input: {query: str, user_id: str}
'''
@app.route('/query', methods=['POST'])
def query():
  body = request.get_json()
  query = body['query']
  user_id = body['user_id']
  
  # Run the query through the 'choose_query' function
  function_call = choose_query_from_prompt(query)
  if not function_call:
    return
  
  function_name = function_call['name']
  function_arguments = function_call['arguments']
  
  if function_name == 'make_sql_query':
    pass
  elif function_name == 'make_content_vector_db_query':
    
    topic = function_arguments.get('topic', None)
    start_time = function_arguments.get('start_time', None)
    end_time = function_arguments.get('end_time', None)
    
    query_result = query_pinecone(query, user_id, top_k = 5)
    
    
  
  return function_call
  
  
