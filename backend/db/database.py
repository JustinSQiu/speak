import sqlite3
import pinecone
import numpy as np
import pandas as pd

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
            transcript_text TEXT,
            {emotion_columns} TEXT
        )
    ''')

def initEmotionsTable():
    pinecone.create_index("hume-emotion", dimension=48)

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
    for response in responses.matches:
        cursor.execute("SELECT * FROM Sentences WHERE sentence_id = ?", (response.id,))
        rows = cursor.fetchall()
    return rows

def rankExperiences(ids):
    pass

if __name__ == '__main__':
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    pinecone.init(api_key="2d619f01-148b-4a3a-9bbf-4b8211f8409d", environment="asia-southeast1-gcp-free")
    index = pinecone.Index("hume-emotion")
    # initMetadataTable(cursor)
    # initEmotionsTable()
    # insertEmotion(index)
    query = [0.1] * 48
    print(getRelevantCommandIds(index, query, 3))


    # Commit the changes and close the connection
    conn.commit()
    conn.close()