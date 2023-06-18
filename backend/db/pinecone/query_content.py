import pinecone
from utils import embed_segments_openai
from constants import PINECONE_API_KEY


# Previously Modal function. Now running here using OpenAI Embedding
def query_pinecone(query: str, user_id: str, top_k: int = 3):
    
    # Connect to Pinecone vector database
    index_id = 'hume-content'
    
    pinecone.init(
      api_key = PINECONE_API_KEY,
      environment = "us-west1-gcp"
    )
    index = pinecone.Index(index_id)
    query_emb = embed_segments_openai([query])[0] # 1 x 1536
      
    # Query Pinecone
    topk_matches = index.query(
      vector = query_emb, 
      filter = {
          'user_id': user_id
      },
      top_k = top_k, 
      include_metadata=True)
        
    topk_matches = topk_matches['matches']
    
    return topk_matches