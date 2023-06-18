
from langchain.embeddings import OpenAIEmbeddings
import os
os.environ["OPENAI_API_KEY"] = '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'

# Batch embedding of segments using OpenAI embeddings - returns a np array (num_sentences x 1536)
def embed_segments_openai(sentences):
  openai_embed = OpenAIEmbeddings() # Size of embeds: (num_chunks x 1536)
  sentences_embeds = openai_embed.embed_documents(sentences)
  return sentences_embeds