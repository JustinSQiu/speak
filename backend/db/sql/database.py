import sqlite3
import pinecone
from constants import EMOTIONS
# import numpy as np
# import pandas as pd

pinecone.init(api_key="2d619f01-148b-4a3a-9bbf-4b8211f8409d", environment="asia-southeast1-gcp-free")

def initMetadataTable(cursor):
    sql_query = f'''
        CREATE TABLE Sentence (
            user_id TEXT,
            entry_id TEXT,
            topic_id TEXT,
            sentence_id TEXT,
            video_link TEXT,
            timestamp INTEGER,
            start_time TEXT,
            end_time TEXT,
            transcript_text TEXT
            + ''' + ', '.join([f'{name} FLOAT' for name in EMOTIONS]) + ''')'''
    print(sql_query)
    cursor.execute(sql_query)
    
            
def initEmotionsTable():
    pinecone.create_index("hume-emotion", dimension=48)

def insertEmotion(data, meta):
    user_id = meta["user_id"]
    entry_id = meta["entry_id"]
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()
 
    index = pinecone.Index("hume-emotion")
    sentence_ids = [f'{user_id}-{entry_id}-{item["sentence_num"]}' for item in range(len(data))]
    sentences_embeds = data["emotions"]
    to_upsert = list(zip(sentence_ids, sentences_embeds))
    for i in range(0, len(to_upsert), 10):
        to_upsert_batch = to_upsert[i:i+10]
        index.upsert(to_upsert_batch)

    for item in data:
        timestamp = f"{meta['date']} {meta['time']}"
        sentence_id = f'{user_id}-{entry_id}-{item["sentence_num"]}'
        transcript_text = item['text']

        emotion_values = ', '.join(['?' for _ in range(48)])

        cursor.execute('''
            INSERT INTO Sentences (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, transcript_text,
                start_time, end_time, ''' + ', '.join([f'emotion{i}' for i in range(1, 49)]) + ''')
            VALUES (?, ?, NULL, ?, NULL, ?, ?, NULL, NULL, ?, ''' + emotion_values + ''')
        ''', (user_id, entry_id, sentence_id, timestamp, transcript_text) + tuple(item['emotion_values']))

    conn.commit()
    conn.close()


def getRelevantCommandIds(index, vector, top_k, cursor):
    responses = index.query(
        vector=vector,
        top_k=top_k,
        include_values=True
    )
    res = []
    for response in responses.matches:
        cursor.execute("SELECT * FROM Sentences WHERE sentence_id = ?", (response.id,))
        rows = cursor.fetchall()
        if rows is not None and len(rows) != 0:
            res.append({
                "result": rows,
                "score": response.score,
            })
    return res

def rankExperiences(rows):
    print(rows)
    topicRanks = {}
    for row in rows:
        if row['result'][0][2] not in topicRanks:
            topicRanks[row['result'][0][2]] = 1
        else:
            topicRanks[row['result'][0][2]] += 1
    return sorted(topicRanks.items(), key=lambda x: x[0])


def rank_topics(sentences, topic_sentences, top_k):
    topic_ranks = {}  # Dictionary to store topic ranks

    # Calculate aggregate rank for each topic
    for topic, sentences_in_topic in topic_sentences.items():
        aggregate_rank = sum(sentences[index] for index in sentences_in_topic)
        topic_ranks[topic] = aggregate_rank

    # Sort topics based on aggregate ranks
    sorted_topics = sorted(topic_ranks.items(), key=lambda x: x[1], reverse=True)

    # Retrieve the top-ranked topics
    top_ranked_topics = [topic for topic, _ in sorted_topics[:top_k]]

    return top_ranked_topics

if __name__ == '__main__':
    conn = sqlite3.connect('metadata.db')
    cursor = conn.cursor()

    # pinecone.init(api_key="2d619f01-148b-4a3a-9bbf-4b8211f8409d", environment="asia-southeast1-gcp-free")
    # index = pinecone.Index("hume-emotion")
    initMetadataTable(cursor)
    # initEmotionsTable()
    # insertEmotion(index)
    # query = [0.1] * 48
    # rows = getRelevantCommandIds(index, query, 3, cursor)
    # print(rankExperiences(rows))

    conn.commit()
    conn.close()