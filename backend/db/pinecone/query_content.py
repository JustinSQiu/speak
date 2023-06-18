import pinecone
from utils import embed_segments_openai
from constants import PINECONE_API_KEY_CONTENT


# Previously Modal function. Now running here using OpenAI Embedding
def query_pinecone_content(query: str, user_id: str, top_k: int = 3):
  
    print(f'query_pinecone: {query}, {user_id}, {top_k}')
    
    pinecone.init(
      api_key = PINECONE_API_KEY_CONTENT,
      environment = "us-west1-gcp"
    )
    index = pinecone.Index('hume-content')
    query_emb = embed_segments_openai([query])[0] # 1 x 1536
      
    # Query Pinecone
    topk_matches = index.query(
      vector = query_emb, 
      filter = {
          'user_id': user_id
      },
      top_k = top_k, 
      include_metadata=True)
    
    # Convert QueryResponse to dict
    topk_matches = topk_matches.to_dict()

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