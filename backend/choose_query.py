import langchain
import openai
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage
import os


function_descriptions = [
  {
    'name': 'make_sql_query',
    'description': 'Used to answer queries primarily involving specific times or time ranges (e.g. past month), or these specific emotions: happy, sad, angry, fearful, disgusted, surprised',
    'parameters': {
      'type': 'object',
      'properties': {
        'emotion': {
        'type': 'string',
        'description': 'The specific emotion that the user wants to query about. The word mentioned in the prompt must exactly match one of the words in the enum list',
        "enum": ["happy", "sad", "angry", "fearful", "disgusted", "surprised"]
        },
        'start_time': {
          'type': 'integer',
          'description': 'The start time of the time range that the user wants to query about. Expressed as the number of days before today. Give no answer if not mentioned'
        },
        'end_time': {
          'type': 'integer',
          'description': 'The end time of the time range that the user wants to query about. Expressed as the number of days before today. Give no answer if not mentioned'
        },
      },
      'required': ['emotion']
    }
  },
  {
    'name': 'make_content_vector_db_query',
    'description': 'Used to answer queries primarily about a topic or experience e.g. playing sports, going on holiday with family, where semantic search is used to find the most relevant context',
    'parameters': {
      'type': 'object',
      'properties': {
        'topic': {
        'type': 'string',
        'description': 'The topic or experience with which the user wants to query relevant experiences using semantic search',
        },
        'start_time': {
          'type': 'integer',
          'description': 'The start time of the time range that the user wants to query about. Expressed as the number of days before today. Give no answer if not mentioned'
        },
        'end_time': {
          'type': 'integer',
          'description': 'The end time of the time range that the user wants to query about. Expressed as the number of days before today. Give no answer if not mentioned'
        },
      },
      'required': ['topic']
    }
  },
  {
    'name': 'make_emotion_vector_db_query',
    'description': 'Used to answer queries which involve emotions which are not exact matches of the words: happy, sad, angry, fearful, disgusted, surprised',
    'parameters': {
      'type': 'object',
      'properties': {
        'emotion': {
        'type': 'string',
        'description': 'The topic or experience with which the user wants to query relevant experiences using semantic search',
        },
        'start_time': {
          'type': 'integer',
          'description': 'The start time of the time range that the user wants to query about. Expressed as the number of days before today. Give no answer if not mentioned'
        },
        'end_time': {
          'type': 'integer',
          'description': 'The end time of the time range that the user wants to query about. Expressed as the number of days before today. Give no answer if not mentioned'
        },
      },
      'required': ['emotion']
    }
  }
]

def choose_query_from_prompt(prompt):

  llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
  in_messages = [HumanMessage(content = prompt)]
  out_message = llm._generate(messages=in_messages, functions = function_descriptions, function_call = 'auto')
  ai_message = out_message.generations[0].message
  
  if 'function_call' in ai_message.additional_kwargs:
    function_name = ai_message.additional_kwargs['function_call']['name']
    # Returns dictionary of name, arguments
    function_arguments = eval(ai_message.additional_kwargs['function_call']['arguments'])
    return {
      'name': function_name,
      'arguments': function_arguments,
    }
  else:
    return None
