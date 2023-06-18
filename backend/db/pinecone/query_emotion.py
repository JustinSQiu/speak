import pinecone
from constants import PINECONE_API_KEY_EMOTION


# Previously Modal function. Now running here using OpenAI Embedding
def query_pinecone_emotion(emotion_emb, user_id: str, top_k: int = 3):
    
    pinecone.init(
      api_key = PINECONE_API_KEY_EMOTION,
      environment = "asia-southeast1-gcp-free"
    )
    index = pinecone.Index('hume-emotion')
      
    # Query Pinecone
    topk_matches = index.query(
      vector = emotion_emb, 
      filter = {
          'user_id': user_id
      },
      top_k = top_k, 
      include_metadata=True)
    
    # Convert QueryResponse to dict
    topk_matches = topk_matches.to_dict()
    
    print(topk_matches)

    matches_processed = [
      {
        'user_id': match['metadata']['user_id'],
        'entry_id':  match['metadata']['entry_id'],
        'sentence_id': match['metadata']['sentence_id'],
        'text': match['metadata']['text'],
        'score': match['score']
      } for match in topk_matches['matches']
    ]
    
            
    return matches_processed