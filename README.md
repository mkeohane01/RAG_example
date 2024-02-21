# Retrieval Augmented Generation - Homework
Implementing custom implementation of RAG without packages such as Langchain or vector databases with built in search such as Pinecone.

Using Magic The Gathering complete rules PDF as the document to retrieve information from.

## Steps
- Extract text data - chunking.py
    - Using PyPDF2 to read PDF in to praseable text.
- Chunk it - chunking.py
    - Chunking with max tokens of 700 yet first looking to split on paragraphs and then at sentances.
- Create Embeddings - embedding_saving.py
    - Embedding each chunk using OpenAI's text-embedding-3-small
- Store chunks with embeddings in a database - embedding_saving.py
    - Stored chunks with embeddings in to local sqlite database
- Perform a retrieval using semantic search - retreival.py 
    - Calculated the cosine similarity between the embedding prompt and each chunk, then pulled the top-n best matches.
- Insert relevant context into the LLM prompt - model.py
    - Passed chunks to context of GPT 3.5 turbo with prompt only to use the context if it applies to the question.

## Results

The Retrieval aspect worked well for this project. I was able to sucessfully find chunks that match the input query. All in all though I found that the RAG could sometimes mislead the model. Also because GPT 3.5 was pre-trained with MTG data (game from the 90s), RAG only out performed on questions about mechanics from the most recent set releases.

### Evaluation
To evaluate I asked a variety of yes/no questions to both the model with and without RAG. I found that the RAG got 7/10 correct while the non-RAG got 6/10 correct. I was surprised because even when it pulled corresponding chunks for some new mechanics (for example The Ring and Battle mechanics), the model still claimed that those didn't exist.

| Input Question                                                                                                   | True Answer | Response with RAG | Response without RAG |
|------------------------------------------------------------------------------------------------------------------|-------------|-------------------|----------------------|
| Is Discover a keyword in MTG?                                                                                    | Yes         | Yes               | No                   |
| Does casting a spell with Foretell from exile allow you to bypass timing restrictions, such as casting a sorcery on an opponent's turn? | No          | No                | No                   |
| Can a player cast the Adventure part of a creature card from their graveyard if it has Flashback?                | No          | No                | No                   |
| Is it possible to choose not to pay the Phyrexian mana cost with life if you have enough mana to pay the cost traditionally? | Yes         | Yes               | Yes                  |
| If a creature card has both Daybound and Nightbound, can it be transformed by effects that do not involve the day/night mechanic? | No          | Yes               | No                   |
| Can the Cleave mechanic be used to modify the text of a creature spell?                                          | No          | No                | No                   |
| Does exiling a card with Escape prevent it from being cast using its Escape ability later?                       | No          | No                | No                   |
| Is it possible to cast a spell with Convoke without tapping any creatures?                                       | Yes         | Yes               | No                   |
| Are battles a card subtype?                                                                                      | Yes         | No                | No                   |
| Is The Ring and tempting a mechanic in MTG?                                                                      | Yes         | No                | No                   |





## To Use
Note: requires a .env file with
```
OPENAI_API_KEY='insertkeyhere'
```
Then after setting up enviornment and installing requirements:
```bash 
pip install -r requirements.txt
python src/flaskserver.py
```
