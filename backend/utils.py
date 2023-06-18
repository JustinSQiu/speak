from langchain.embeddings import OpenAIEmbeddings
from enum import Enum
import os
from datetime import datetime

os.environ["OPENAI_API_KEY"] = "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"


# Batch embedding of segments using OpenAI embeddings - returns a np array (num_sentences x 1536)
def embed_segments_openai(sentences):
    openai_embed = OpenAIEmbeddings()  # Size of embeds: (num_chunks x 1536)
    sentences_embeds = openai_embed.embed_documents(sentences)
    return sentences_embeds


def combine_date_and_time(date_str, time_str):
    datetime_str = f"{date_str} {time_str}"
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    formatted_datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime_str


# Works for all types of entries
def create_sentences(segments_data, MIN_WORDS, MAX_WORDS):
    # Combine the non-sentences together
    sentences = []

    is_new_sentence = True
    sentence_length = 0
    sentence_num = 0
    sentence_segments = []

    for i in range(len(segments_data)):
        if is_new_sentence == True:
            is_new_sentence = False
        # Append the segment
        sentence_segments.append(segments_data[i]["text"])
        segment_words = segments_data[i]["text"].split(" ")
        sentence_length += len(segment_words)

        # If exceed MAX_WORDS, then stop at the end of the segment
        # Only consider it a sentence if the length is at least MIN_WORDS
        if (
            sentence_length >= MIN_WORDS and segments_data[i]["text"][-1] == "."
        ) or sentence_length >= MAX_WORDS:
            sentence = " ".join(sentence_segments)
            sentences.append(
                {
                    "sentence_num": sentence_num,
                    "text": sentence,
                    "sentence_length": sentence_length,
                    "start_chunk_id": i - len(sentence_segments) + 1,
                    "end_chunk_id": i,
                    "start_time": segments_data[i - len(sentence_segments) + 1].get(
                        "start_time", None
                    ),
                    "end_time": segments_data[i].get("end_time", None),
                }
            )
            # Reset
            is_new_sentence = True
            sentence_length = 0
            sentence_segments = []
            sentence_num += 1

    return sentences


def getCloudUrl(id):
    return f"https://storage.googleapis.com/langchain-embeddings/{id}.json"
