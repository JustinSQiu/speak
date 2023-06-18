import pinecone
from utils import embed_segments_openai
from constants import PINECONE_API_KEY_EMOTION
import os

os.environ["OPENAI_API_KEY"] = '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'

'''  
episode_sentences: list (of number of sentences in an entry) of sentence text
emotion_emds: list (of number of sentences in an entry) of 48-dim list
'''

def upload_emotion_pinecone(sentences_dict, user_id: str, entry_id: str, upload: bool = True):
  # Connect to Pinecone database
  pinecone.init(
      api_key = PINECONE_API_KEY_EMOTION,
      environment = "asia-southeast1-gcp-free"
    )
  index = pinecone.Index("hume-emotion")
  
  sentences = [sentence_dict['text'] for sentence_dict in sentences_dict]
  emotion_embs = [sentence_dict['emotions'] for sentence_dict in sentences_dict]
  
  # Sentences are between 20-30 words long (captures 1 idea)
  sentence_ids = [f'{user_id}-{entry_id}-{sentence_id}' for sentence_id in range(len(emotion_embs))]
  sentences_metadata = [
    {'user_id': user_id, 'entry_id': entry_id, 'sentence_id': sentence_id, 'text': sentence}
    for sentence_id, sentence in enumerate(sentences)
  ]

  to_upsert = list(zip(sentence_ids, emotion_embs, sentences_metadata))
    
  print(f'Uploading to Pinecone, {len(to_upsert)} sentences')
  
  for i in range(0, len(to_upsert), 10):
    to_upsert_batch = to_upsert[i:i+10]
    index.upsert(to_upsert_batch)
    
  print('Upload to Pinecone complete', index.describe_index_stats())



