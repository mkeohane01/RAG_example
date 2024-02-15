import sqlite3

def retrieve_chunks(db_path='rag_data.db', db_query="SELECT id, text FROM chunks"):
    '''
    Retrieves the chunks from the database
    param: db_path - path to the database
    return: list of text chunks
    '''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(db_query)
    chunks = c.fetchall()
    conn.close()
    print(f"{len(chunks)} chunks retrieved from {db_path}.")
    return chunks

if __name__ == '__main__':
    chunks = retrieve_chunks()
    for i, chunk in enumerate(chunks):
        print(f'Chunk {i+1}:\n{chunk}\n')