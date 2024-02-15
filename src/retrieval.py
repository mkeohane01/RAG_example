import sqlite3
import pickle
from embedding_saving import chunk_embedding
import numpy as np

def cosine_similarity(vec1, vec2):
    """Compute the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity

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

def get_chunks_by_similarity(input_query, db_path='rag_data.db', top_n=3):
    '''
    Retrieves the chunks from the database that are similar to the input query
    param: input_query - the query to search for
    param: db_path - path to the database
    return: list of text chunks
    '''
    # Embed the input query
    input_emb = chunk_embedding(input_query)

    # Retrieve the chunks from the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, text, embedding FROM chunks")
    chunks = c.fetchall()
    conn.close()
    print(f"{len(chunks)} chunks retrieved from {db_path}.")

    # Find the best matching chunks
    similarities = []
    for chunk in chunks:
        # Deserialize the chunk's embedding
        emb = pickle.loads(chunk[2])
        # Calculate cosine similarity
        similarity = cosine_similarity(input_emb, emb)
        similarities.append((chunk[0], chunk[1], similarity))

    print(f"{len(similarities)} similarities calculated.")
    # Sort the chunks based on similarity (highest first)
    similarities.sort(key=lambda x: x[2], reverse=True)

    # return the top N chunks with the highest similarity
    best_chunks = similarities[:top_n]

    return best_chunks


if __name__ == '__main__':
    best_chunks = get_chunks_by_similarity("How do I cast a spell?", top_n=3)
    print(best_chunks)