import sqlite3
import backend.db.pinecone.upload_content as upload_content

def initMetadataTable(cursor):
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

def initEmotionsTable():
    upload_content.create_index("hume-emotion", dimension=48)

def insertEmotion():
    index = upload_content.Index("hume-emotion")
    index.upsert([
        ("A", [0.1] * 48)
    ])

if __name__ == '__main__':
    # Connect to the SQLite database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    upload_content.init(api_key="2d619f01-148b-4a3a-9bbf-4b8211f8409d", environment="asia-southeast1-gcp-free")
    # initMetadataTable()
    # initEmotionsTable()
    insertEmotion()

    # Commit the changes and close the connection
    conn.commit()
    conn.close()