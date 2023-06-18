import sqlite3
import pinecone
import numpy as np
import pandas as pd
import langchain
import openai
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

def initMetadataTable(cursor):
    cursor.execute('DROP TABLE IF EXISTS Sentences')

    emotion_columns = ', '.join([f'emotion{i}' for i in range(1, 49)])
    cursor.execute(f'''
        CREATE TABLE Sentences (
            user_id TEXT,
            entry_id TEXT,
            topic_id TEXT,
            sentence_id TEXT,
            video_link TEXT,
            timestamp INTEGER,
            start_time TEXT,
            end_time TEXT,
            transcript_text TEXT
            {emotion_columns} TEXT
        )
    ''')

    user_id = "userhello"
    entry_id = "entry456"
    topic_id = "hello789"
    sentence_id = "B"
    video_link = "hello"
    timestamp = 123
    start_time = "00:00:10"
    end_time = "00:00:20"
    transcript_text = "This is a test sentence."
    emotion_values = [0.1] * 48
    cursor.execute("INSERT INTO Sentences (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, start_time, end_time, transcript_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, start_time, end_time, transcript_text))


    user_id = "user123"
    entry_id = "entry456"
    topic_id = "hello789"
    sentence_id = "A"
    video_link = "hello"
    timestamp = 123
    start_time = "00:00:10"
    end_time = "00:00:20"
    transcript_text = "This is a test sentence."
    emotion_values = [0.1] * 48
    cursor.execute("INSERT INTO Sentences (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, start_time, end_time, transcript_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, start_time, end_time, transcript_text))


    user_id = "user123"
    entry_id = "entry456"
    topic_id = "hellonot7990"
    sentence_id = "C"
    video_link = "hello"
    timestamp = 123
    start_time = "00:00:10"
    end_time = "00:00:20"
    transcript_text = "This is a test sentence."
    emotion_values = [0.1] * 48
    cursor.execute("INSERT INTO Sentences (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, start_time, end_time, transcript_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (user_id, entry_id, topic_id, sentence_id, video_link, timestamp, start_time, end_time, transcript_text))

def initEmotionsTable():
    pinecone.create_index("hume-emotion", dimension=48)

# TODO: load metadata and embedding in SQLite and Pinecone; this is placeholder data
def insertEmotion(index):
    index.upsert([
        ("A", np.concatenate((np.ones(24), np.zeros(24))).tolist()),
        ("B", [1] * 48),
        ("C", np.random.rand(48,).tolist()),
    ])

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

# TODO: add chunk with mean, adjust this experience ranker
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

# NOTE: my work is in another file, will push it tmr but it's not completely working rn. shouldn't be relevant for your guys data integration
def sqlAgentQuery():
    db = SQLDatabase.from_uri("sqlite:///titanic.db")
    llm = OpenAI(temperature=0)
    db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
    db_chain.run("what sentences have id that is 'a'?")


if __name__ == '__main__':
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    pinecone.init(api_key="2d619f01-148b-4a3a-9bbf-4b8211f8409d", environment="asia-southeast1-gcp-free")
    index = pinecone.Index("hume-emotion")
    initMetadataTable(cursor)
    # initEmotionsTable()
    # insertEmotion(index)
    query = [0.1] * 48
    rows = getRelevantCommandIds(index, query, 3, cursor)
    print(rankExperiences(rows))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()