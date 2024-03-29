from openai import Client
import dotenv
from retrieval import get_chunks_by_similarity

dotenv.load_dotenv()

def prompt_gpt(prompt, chunks, model="gpt-3.5-turbo", temp=0.7, max_tok=300):
    """
    This function prompts GPT-3.5-turbo as a judge for a Magic: The Gathering tournament.
    Args:
        prompt: a string of text
        chunks: a list of text chunks
        model: the model to use
    Returns:
       rag_response: a string of text using RAG
       basic_response: a string of text wihoout RAG
    """
    client = Client()
    # Create the context based on the chunks
    context = "Here are chunks similar to the query from MTG rules. Use them to guide your response if they truthfully align with the prompt:\n\n"
    for chunk in chunks:
        context += chunk[1] + "\n"

    # Build system for MTG bot
    system = "Answer questions factucally as a judge for a Magic: The Gathering tournament."

    # Generate the response from gpt api with RAG
    rag_response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "assistant",
                "content": context,
            }
        ],
            model=model,
            temperature=temp,  
            max_tokens=max_tok  
        )
   # Generate the response from gpt api without RAG
    basic_response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
            model=model,
            temperature=temp,  
            max_tokens=max_tok  
        ) 
   
    return rag_response.choices[0].message.content, basic_response.choices[0].message.content


if __name__ == '__main__':
    query = "What happens when a creature dies?"
    chunks = get_chunks_by_similarity(query)
    print(chunks)
    response = prompt_gpt(query, chunks)
    print(response)