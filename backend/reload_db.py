# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect("backend/memos.db")
# cursor = conn.cursor()

# # Drop the existing table if it exists
# cursor.execute("DROP TABLE IF EXISTS entries")

# # Create a new table with the desired columns
# create_table_query = """
# CREATE TABLE entries (
#     id VARCHAR(255) PRIMARY KEY,
#     time VARCHAR(255),
#     date VARCHAR(255),
#     type VARCHAR(255)
# );
# """
# cursor.execute(create_table_query)

# print("Done")

# # Commit the changes and close the connection
# conn.commit()
# conn.close()
