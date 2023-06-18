
import json
import os
import pandas as pd
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAIChat
from langchain.schema import HumanMessage, AIMessage, ChatMessage

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
import networkx as nx
from networkx.algorithms import community

import asyncio
from datetime import datetime

os.environ['OPENAI_API_KEY'] = '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'


async def async_generate(llm, prompt):
  resp = await llm.agenerate([prompt])
  return resp.generations[0][0].text

async def generate_concurrently(llm, prompts):
  tasks = [async_generate(llm, prompt) for prompt in prompts]
  out = await asyncio.gather(*tasks)
  return out


'''
Inputs: 
- entries_sentences: List of n_entries, each element is a list of n_sentences, each element is a dict with 'text' and 'time'
- entries_embeds: List of n_entries, each element is a list of n_sentences, each element is a 1536-dim vector

Output:
- entries_topics: List, each entry {entry_id, topic_id, sentence_ids, sentences, title} i.e. a list of topics for all entries combined
'''
def run_clustering(entries_sentences, entries_embeds):
  
  # Calculate similarity matrices for each entry
  entries_embeds = [np.array(entry_embeds) for entry_embeds in entries_embeds]
  
  print('entries_embeds', entries_embeds[0].shape)
    
  # entries_similarity_matrices: List of n_entries, each element is a n_sentences x n_sentences similarity matrix
  entries_similarity_matrices = [get_similarity_matrix(entry_embeds) for entry_embeds in entries_embeds]
  
  print('entries_similarity_matrices', entries_similarity_matrices[0].shape)
  
  # Conduct community-finding to get clusters of sentences
  # entries_communities: List of n_entries, each element is dict with 'community_sentence' and 'sentence_community'
  entries_communities = [get_communities(entry_similarity_matrix, num_communities = np.floor(np.sqrt(entry_similarity_matrix.shape[0])), bonus_constant = 0.1, min_size = 2, num_iterations = 20) 
                        for entry_similarity_matrix in entries_similarity_matrices]
  
  print('entries_communities', entries_communities[0]['community_sentence'])
  
  # entries_topics_sentences: List of n_entries, each element is a list of n_communities, each element is a list of sentences in that community

  entries_topics = []
  for entry_id, entry_communities in enumerate(entries_communities):
    for comm_id, comm_sentence_ids in enumerate(entry_communities['community_sentence']):
      # Get the sentences in that community
      print(entry_id, entry_communities, comm_id, comm_sentence_ids)
      sentences = [entries_sentences[entry_id][sentence_id]['text'] for sentence_id in comm_sentence_ids]
      entry_topic = {
        'entry_id': entry_id,
        'topic_id': comm_id,
        'sentence_ids': sorted(comm_sentence_ids),
        'sentences': sentences
      }
      print(entry_topic)
      entries_topics.append(entry_topic)
      
  # Generate titles for each topic
  entries_topics = generate_topic_titles(entries_topics)
  
  return entries_topics
  
  
  
  
  
##### HELPER FUNCTIONS

def generate_topic_titles(entries_topics):
  '''
  Input: entries_topics: List[dict] - list of topics, each topic is {entry_id, topic_id, sentence_ids, sentences}
  (Modifies entries_topics to add in title)
  Output: entries_topics
  '''
  
  # Convert entries_topics to a list of sentences for each topic
  topics_sentences = [topic['sentences'] for topic in entries_topics]
  # Concat sentences for each topic
  topics_concat = ['\n'.join(topic_sentences) for topic_sentences in topics_sentences]
  
  # Prompt that passes in all the titles of a topic, and asks for an overall title of the topic
  prompts = [f"""Write an informative, concise title of ~5 words that summarizes the main idea of the following sentences, which come from a personal journal.
             
             EXAMPLES OF GOOD TITLES:
             1. Lost football competition
             2. argued with brother about chores
             3. Fun experience at the beach
             
     SENTENCES:        
    {topic_concat}

    CONCISE TITLE:"""  for topic_concat in topics_concat]
  
  print(f'Number of prompts: {len(prompts)}')
  
  print(f'Started at: {datetime.now()}')
    
  llm = OpenAIChat(temperature=0.1, model="gpt-3.5-turbo-0613")
  titles = asyncio.run(generate_concurrently(llm, prompts))
  
  print(f'Finished at: {datetime.now()}')

  # Add titles to entries_topics 
  for i, topic in enumerate(entries_topics):
    topic['title'] = titles[i]

  return entries_topics

'''   
Inputs: 
similarity_mat: n_sentences x n_sentences matrix of cosine similarity between sentences

Outputs:
community_sentence: List of communities, each community is a list of sentence indices
sentence_community: List of sentence indices, each index is the community it belongs to
'''
def get_communities(similarity_mat, num_communities = 4, bonus_constant = 0.25, min_size = 2, num_iterations = 40):

  proximity_bonus_arr = np.zeros_like(similarity_mat)
  for row in range(proximity_bonus_arr.shape[0]):
    for col in range(proximity_bonus_arr.shape[1]):
      if row == col:
        proximity_bonus_arr[row, col] = 0
      else:
        proximity_bonus_arr[row, col] = 1/(abs(row-col)) * bonus_constant
        
  similarity_mat += proximity_bonus_arr

  title_nx_graph = nx.from_numpy_array(similarity_mat)

  desired_num_communities = num_communities
  # Store the accepted partitionings
  communities_title_accepted = []

  resolution = 0.6
  resolution_step = 0.01
  iterations = num_iterations

  # Find the resolution that gives the desired number of communities
  communities_title = []
  while len(communities_title) not in [desired_num_communities, desired_num_communities + 1, desired_num_communities + 2]:
    communities_title = community.louvain_communities(title_nx_graph, weight = 'weight', resolution = resolution)
    resolution += resolution_step
  # communities_title_accepted.append(communities_title)
  community_sizes = [len(c) for c in communities_title]
  sizes_sd = np.std(community_sizes)
  modularity = community.modularity(title_nx_graph, communities_title, weight = 'weight', resolution = resolution)

  # print(f'Iteration 0: {modularity}, Number of communities: {len(communities_title)}')
  # print('Community sizes', community_sizes, 'SD,' , np.std(community_sizes))
  # print(f'Resolution: {resolution}')

  lowest_sd_iteration = 0
  # Set lowest sd to inf
  lowest_sd = float('inf')

  for i in range(iterations):
    communities_title = community.louvain_communities(title_nx_graph, weight = 'weight', resolution = resolution)
    modularity = community.modularity(title_nx_graph, communities_title, weight = 'weight', resolution = resolution)
    
    # Check SD
    community_sizes = [len(c) for c in communities_title]
    sizes_sd = np.std(community_sizes)
    
    communities_title_accepted.append(communities_title)
    
    # print(f'Iteration {i + 1}: {modularity}, Number of communities: {len(communities_title)}')
    # print('Community sizes', community_sizes, 'SD,' , np.std(community_sizes), 'Min', min(community_sizes))
    
    if sizes_sd < lowest_sd and min(community_sizes) >= min_size:
      lowest_sd_iteration = i
      lowest_sd = sizes_sd
      
  # Set the chosen partitioning to be the one with highest modularity
  communities_title = communities_title_accepted[lowest_sd_iteration]
  # print(f'Best SD: {lowest_sd}, Best iteration: {lowest_sd_iteration}')
  
  community_id_means = [sum(e)/len(e) for e in communities_title]
  # Arrange title_communities in order of community_id_means
  communities_title = [list(c) for _, c in sorted(zip(community_id_means, communities_title), key = lambda pair: pair[0])]
  print('communities_title', communities_title)
  # Create an array denoting which community each chunk belongs to
  chunk_communities = [None] * similarity_mat.shape[0]
  for i, c in enumerate(communities_title):
    for j in c:
      chunk_communities[j] = i
      
  # print('chunk communities', chunk_communities)
      
  return {
    'community_sentence': communities_title,
    'sentence_community': chunk_communities
  }
  
# Plot a heatmap of this array
def plot_communities(sentence_communities):
  plt.figure(figsize = (10, 3))
  plt.imshow(np.array(sentence_communities).reshape(1, -1), cmap = 'tab20')
  # Draw vertical black lines for every 1 of the x-axis 
  for i in range(1, len(sentence_communities)):
    plt.axvline(x = i - 0.5, color = 'black', linewidth = 0.5)
    
''' 
Input: list of 1536-dim vectors representing each sentence
Output: n x n matrix of cosine similarity between each pair of sentences
'''

def get_similarity_matrix(embeds):
  # Embeds is n x 1536 vector
  n_vectors = embeds.shape[0]
  cosine_sim = np.zeros((n_vectors, n_vectors))

  # calculate cosine similarity between all pairs of sentences
  for i in range(n_vectors):
    cosine_sim[i, i] = 1
    for j in range(i+1, n_vectors):
      similarity = 1 - cosine(embeds[i], embeds[j])
      cosine_sim[i, j] = similarity
      cosine_sim[j, i] = similarity
      
  return cosine_sim

