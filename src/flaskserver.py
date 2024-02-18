from flask import Flask, request, jsonify
from retrieval import get_chunks_by_similarity
from model import prompt_gpt

app = Flask(__name__)

from flask import Flask, request, jsonify, render_template
from retrieval import get_chunks_by_similarity
from model import prompt_gpt

app = Flask(__name__)

@app.route('/')
def index():
    '''
    This function renders the HTML interface for the RAG model.
    '''
    return render_template('index.html')

@app.route('/rag', methods=['POST'])
def retrieval_augmented_generation():
    '''
    This function retrieves the most similar chunks from the database, 
    passes them to the GPT-3 model, and returns the generated text.
    '''
    # Get the input query
    input_query = request.json['query']
    print(f"Received query: {input_query}")

    # Retrueve number of chunks to retreive
    if 'num_chunks' in request.json:
        top_n = request.json['num_chunks']
    else:
        top_n = 3

    # Retrieve the most similar chunks from the database
    best_chunks = get_chunks_by_similarity(input_query, top_n=top_n)
    print(f"Retrieved {len(best_chunks)} chunks.")
    for chunk in best_chunks:
        print(chunk[1])

    # Prompt the model with the input query and the best chunks
    response = prompt_gpt(input_query, best_chunks)

    return jsonify({'response': response, 'chunks': best_chunks})
    
if __name__ == '__main__':
    app.run(debug=True)