import pinecone
from utils import embed_segments_openai
from constants import PINECONE_API_KEY
import os

pinecone.init(api_key = PINECONE_API_KEY, environment = 'us-west1-gcp')

os.environ["OPENAI_API_KEY"] = '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'


def embed_transcript_upload_pinecone(episode_sentences, user_id: str, entry_id: str):
  # Connect to Pinecone database
  index = pinecone.Index("hume-content")
  
  # Sentences are between 30-60 words long (captures 1 idea)
  sentence_ids = [f'{user_id}-{entry_id}-{sentence_id}' for sentence_id in range(len(episode_sentences))]
  sentences_metadata = [
    {'user_id': user_id, 'entry_id': entry_id, 'sentence_id': sentence_id, 'text': sentence}
    for sentence_id, sentence in enumerate(episode_sentences)
  ]
  
  print(sentence_ids, sentences_metadata)
  sentences_embeds = embed_segments_openai(episode_sentences)
  
  to_upsert = list(zip(sentence_ids, sentences_embeds, sentences_metadata))
    
  print(f'Uploading to Pinecone, {len(to_upsert)} sentences')
  
  for i in range(0, len(to_upsert), 10):
    to_upsert_batch = to_upsert[i:i+10]
    index.upsert(to_upsert_batch)
    
  print('Upload to Pinecone complete', index.describe_index_stats())
  return sentences_embeds



