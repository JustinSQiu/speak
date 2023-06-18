import pinecone
import os
from langchain.embeddings import OpenAIEmbeddings


pinecone.init(api_key = 'b183d65d-9501-483a-82e7-8e86f9eb46ce', environment = 'us-west1-gcp')

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
  
  print(to_upsert)
  
  print(f'Uploading to Pinecone, {len(to_upsert)} sentences')
  
  for i in range(0, len(to_upsert), 10):
    to_upsert_batch = to_upsert[i:i+10]
    index.upsert(to_upsert_batch)
    
  print('Upload to Pinecone complete', index.describe_index_stats())


# Batch embedding of segments using OpenAI embeddings - returns a np array (num_sentences x 1536)
def embed_segments_openai(sentences):
  openai_embed = OpenAIEmbeddings() # Size of embeds: (num_chunks x 1536)
  sentences_embeds = openai_embed.embed_documents(sentences)
  return sentences_embeds

def create_sentences(segments, MIN_WORDS, MAX_WORDS):

  # Combine the non-sentences together
  sentences = []

  is_new_sentence = True
  sentence_length = 0
  sentence_num = 0
  sentence_segments = []

  for i in range(len(segments)):
    if is_new_sentence == True:
      is_new_sentence = False
    # Append the segment
    sentence_segments.append(segments[i])
    segment_words = segments[i].split(' ')
    sentence_length += len(segment_words)
    
    # If exceed MAX_WORDS, then stop at the end of the segment
    # Only consider it a sentence if the length is at least MIN_WORDS
    if (sentence_length >= MIN_WORDS and segments[i][-1] == '.') or sentence_length >= MAX_WORDS:
      sentence = ' '.join(sentence_segments)
      sentences.append({
        'sentence_num': sentence_num,
        'text': sentence,
        'sentence_length': sentence_length
      })
      # Reset
      is_new_sentence = True
      sentence_length = 0
      sentence_segments = []
      sentence_num += 1

  return sentences

