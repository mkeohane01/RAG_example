import sqlite3
import openai
from chunking import chunk_text, extract_text_from_pdf
import dotenv
import pickle

dotenv.load_dotenv()

def setup_sqlite_db(db_path='rag_data.db', remove_existing=True):
    '''
    Creates the database to store the text chunks
    '''
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if remove_existing:
        c.execute('''DROP TABLE IF EXISTS chunks''')
    c.execute('''CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, text TEXT, embedding BLOB)''')
    conn.commit()
    conn.close()
    print(f"Database created at {db_path}.")
    return db_path

def chunk_embedding(chunk, model="text-embedding-3-small"):
    """
    This function create the embeddings from Open AI
    Args:
        chunk: a string of text
    Returns:
        a vector of embeddings for the chunk
    """
    # Create an OpenAI client
    client = openai.Client()
    # Create the embeddings
    embeddings = client.embeddings.create(input=[chunk], model=model).data[0].embedding
    print(f"Embedding created for chunk: {chunk[:50]}...")
    return embeddings

def store_chunks(chunks, db_path='rag_data.db', remove_existing=False):
    '''
    Stores the chunks in the database
    param: chunks - list of text chunks
    '''
    db = setup_sqlite_db(db_path, remove_existing)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for chunk in chunks:
        emb = chunk_embedding(chunk)
        emb_blob = pickle.dumps(emb)
        print(emb_blob[:5])
        c.execute("INSERT INTO chunks (text, embedding) VALUES (?, ?)", (chunk, emb_blob))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    pdf_path = './pdfs/MagicCompRules.pdf'
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, 700, True)
    store_chunks(chunks, db_path='rag_data.db', remove_existing=True)
    print("Chunks stored in the database.")