from langchain.embeddings import OpenAIEmbeddings
from enum import Enum
import os

os.environ["OPENAI_API_KEY"] = "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"


# Batch embedding of segments using OpenAI embeddings - returns a np array (num_sentences x 1536)
def embed_segments_openai(sentences):
    openai_embed = OpenAIEmbeddings()  # Size of embeds: (num_chunks x 1536)
    sentences_embeds = openai_embed.embed_documents(sentences)
    return sentences_embeds


# Works for all types of entries
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
        segment_words = segments[i].split(" ")
        sentence_length += len(segment_words)

        # If exceed MAX_WORDS, then stop at the end of the segment
        # Only consider it a sentence if the length is at least MIN_WORDS
        if (
            sentence_length >= MIN_WORDS and segments[i][-1] == "."
        ) or sentence_length >= MAX_WORDS:
            sentence = " ".join(sentence_segments)
            sentences.append(
                {
                    "sentence_num": sentence_num,
                    "text": sentence,
                    "sentence_length": sentence_length,
                    "start_chunk_id": i - len(sentence_segments) + 1,
                    "end_chunk_id": i,
                }
            )
            # Reset
            is_new_sentence = True
            sentence_length = 0
            sentence_segments = []
            sentence_num += 1

    return sentences


def getCloudUrl(id, suffix):
    return f"https://storage.googleapis.com/calhacks-videos/{id}.{suffix}"
