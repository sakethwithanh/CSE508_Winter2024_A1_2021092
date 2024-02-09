import string
import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_input(query):
    tokens = word_tokenize(query)
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token.strip() for token in tokens]
    return tokens

def create_positional_index(documents):
    positional_index = {}
    for doc_id, document in enumerate(documents, start=1):
        tokens = preprocess_input(document)
        for position, token in enumerate(tokens, start=1):
            if token not in positional_index:
                positional_index[token] = {}
            if doc_id not in positional_index[token]:
                positional_index[token][doc_id] = []
            positional_index[token][doc_id].append(position)
    return positional_index

def save_positional_index(index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(index, file)

def load_positional_index(filename):
    with open(filename, 'rb') as file:
        index = pickle.load(file)
    return index

def process_phrase_query(query, positional_index):
    terms = preprocess_input(query)
    if len(terms) == 0:
        return set()

    # Get documents containing the first term
    first_term = terms[0]
    if first_term not in positional_index:
        return set()
    documents = set(positional_index[first_term].keys())

    # Initialize result with documents containing first term
    result = documents.copy()

    # Iterate over terms and update result with documents containing all terms
    for term in terms[1:]:
        if term not in positional_index:
            return set()
        term_documents = set(positional_index[term].keys())
        result = result.intersection(term_documents)

    # Check if the phrase appears in the documents
    for doc_id in result.copy():
        positions = [positional_index[term][doc_id] for term in terms]
        for pos in positions[0]:
            if all(pos + i in positions[i] for i in range(1, len(positions))):
                continue
            else:
                result.remove(doc_id)
                break

    return result

def get_document_names(doc_ids):
    return [f'document_{doc_id}.txt' for doc_id in doc_ids]

# Sample documents
documents = []

directory = r'D:\Studies\SEM6\\Information Retrieval\Assignments\\CSE508_Winter2024_A1_2021092\\processed_text_files'

document_ids = os.listdir(directory)

for doc_id in document_ids:
    with open(os.path.join(directory, doc_id), 'r') as file:
        document_string = ""
        for line in file:
            document_string += line.strip()
            document_string += " "
        documents.append(document_string)

# Create positional index
positional_index = create_positional_index(documents)

# Save the positional index
save_positional_index(positional_index, 'positional_index.pkl')

# Load the positional index
loaded_index = load_positional_index('positional_index.pkl')

# Get number of queries from user
num_queries = int(input("Enter the number of queries: "))

# Process each query and output results
for query_num in range(1, num_queries + 1):
    query = input(f"Enter query {query_num}: ")
    result = process_phrase_query(query, loaded_index)
    print(f"Number of documents retrieved for query {query_num} using positional index: {len(result)}")
    print(f"Names of documents retrieved for query {query_num} using positional index: {', '.join(get_document_names(result))}")
