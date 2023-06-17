import sqlite3
import pinecone

def createMetadataTable():
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
