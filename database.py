import sqlite3
import pinecone

def initMetadataTable():
    # Connect to the SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Define the emotion column names
    emotion_columns = ', '.join([f'emotion{i}' for i in range(1, 49)])

    # Create the "Sentences" table
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


    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def initEmotionsTable():
    pinecone.init(api_key="2d619f01-148b-4a3a-9bbf-4b8211f8409d", environment="test")
    pinecone.create_index("hume-emotion", dimension=48)

def insertEmotion(emotions):
    index = pinecone.Index("hume-emotion")
    for emotion in emotions:
        index.upsert([
            ("A", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
            ("B", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
            ("C", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
            ("D", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]),
            ("E", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
        ])

if __name__ == '__main__':
    initMetadataTable()
    initEmotionsTable()