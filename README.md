# Retrieval Augmented Generation - Homework
Implementing custom implementation of RAG without packages such as Langchain

## Steps
- Extract text data
- Chunk it
- Create Embeddings
- Store chunks with embeddings in a database
- Perform a retrieval using semantic search
- Insert relevant context into the LLM prompt

## To Use
Note: requires a .env file with
```
OPENAI_API_KEY='insertkeyhere'
FLASK_APP=app
```
Then:
```bash 
pip install -r requirements.txt
Flask run
```

## Repo Structure
