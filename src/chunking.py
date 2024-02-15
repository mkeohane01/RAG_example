import PyPDF2

def extract_text_from_pdf(pdf_path):
    '''
    Extracts text from a PDF file
    param: pdf_path - path to the PDF file
    return: text extracted from the PDF file
    '''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    print(f"Text extracted from {pdf_path}.")
    return text

def chunk_text(text, chunk_size, split_newlines=True):
    '''
    Splits the text into chunks, preferably at the end of lines within a buffer range around the specified chunk size.
    If split_newlines is True, it tries to split at the newline closest to the end of the chunk size without exceeding it.
    
    :param text: Text to be split.
    :param chunk_size: Desired size of each chunk.
    :param split_newlines: Whether to prefer splitting the text at newlines.
    :return: List of text chunks.
    '''
    chunks = []
    start = 0
    while start < len(text):
        # Check if we are at the last chunk which might be shorter than chunk_size
        if start + chunk_size > len(text):
            end = len(text)
        else:
            end = start + chunk_size
            # If splitting at newlines, adjust end to the last newline before the chunk would otherwise end
            if split_newlines:
                newline_end = text.rfind('\n', start, end)
                if newline_end != -1:
                    end = newline_end + 1
                else:
                    # If no suitable newline, try to break at a space or stick with the hard limit
                    space_end = text.rfind(' ', start, end)
                    end = space_end + 1 if space_end != -1 else end
        
        chunks.append(text[start:end])
        start = end  # Move start to the end of the last chunk without overlap
    
    print(f"{len(chunks)} chunks created.")
    return chunks


if __name__ == '__main__':
    pdf_path = './pdfs/MagicCompRules.pdf'
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, 500, True)
    for i, chunk in enumerate(chunks):
        print(f'Chunk {i+1}:\n{chunk}\n')
        if i == 10:
            break