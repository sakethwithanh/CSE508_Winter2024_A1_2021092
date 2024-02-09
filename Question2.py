import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import defaultdict

def preprocess_query(query):
    tokens = word_tokenize(query)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def file_not(word, inverted_index):
    answer_set = set()
    for i in range(1, 1000):
        answer_set.add("processed_file"+str(i)+".txt")

    if word not in inverted_index.keys():
        return answer_set
    else:
        for file in inverted_index[word]:
            answer_set.remove(file)

    return answer_set

def process_query(query, operations, inverted_index):
    terms = preprocess_query(query)
    operations = [operation.strip() for operation in operations]
    print(operations)
    if len(operations) != len(terms) - 1:
        print("Error: Number of operations doesn't match the number of terms.")
        return set()  # Return an empty set to indicate an error
    result = set(inverted_index[terms[0]])

    for i in range(1, len(terms)):

        if terms[i] not in inverted_index.keys():
            inverted_index[terms[i]] = set()

        if operations[i-1] == "AND":
            result = result.intersection(set(inverted_index[terms[i]]))
        elif operations[i-1] == "OR":
            result = result.union(set(inverted_index[terms[i]]))
        elif operations[i-1] == "OR NOT":
            result = result.union(file_not(terms[i], inverted_index))
        elif operations[i-1] == "AND NOT":
            result = result.intersection(file_not(terms[i], inverted_index))
    return result

def execute_queries(queries, inverted_index):
    results = []
    for input_sequence, operations in queries:
        result = process_query(input_sequence, operations, inverted_index)
        results.append(result)
    return results

def get_document_names(result):
    return [f'file_{i}.txt' for i in result]

def get_user_queries():
    num_queries = int(input("Enter the number of queries: "))
    queries = []
    for i in range(num_queries):
        print(f"Query {i+1}:")
        input_sequence = input("Input sequence: ")
        operations = input("Operations (comma-separated): ").split(",")
        queries.append((input_sequence, operations))
    return queries


def create_inverted_index(directory):
    inverted_index = defaultdict(set)
    document_ids = os.listdir(directory)
    for doc_id in document_ids:
        with open(os.path.join(directory, doc_id), 'r') as file:
            terms = file.read().strip().split('\n')
            for term in terms:
                if term not in inverted_index:
                    inverted_index[term] = set()
                inverted_index[term].add(doc_id)
    return inverted_index

def save_inverted_index(index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(index, file)

def load_inverted_index(filename):
    with open(filename, 'rb') as file:
        index = pickle.load(file)
    return index
# Load the inverted index from the file
def load_inverted_index(filename):
    with open(filename, 'rb') as file:
        index = pickle.load(file)
    return index

# Load the inverted index
directory = r'D:\Studies\SEM6\\Information Retrieval\Assignments\\CSE508_Winter2024_A1_2021092\\processed_text_files'
unigram_inverted_index = create_inverted_index(directory)

# Save the inverted index to a file
save_inverted_index(unigram_inverted_index, 'unigram_inverted_index.pkl')

# Load the inverted index from the file
loaded_index = load_inverted_index('unigram_inverted_index.pkl')

# Get user queries
queries = get_user_queries()

# Execute queries
results = execute_queries(queries, loaded_index)

# Output results
for idx, (query, result) in enumerate(zip(queries, results), 1):
    print(f"Query {idx}: {query[0]}")
    print(f"Number of documents retrieved for query {idx}: {len(result)}")
    print(f"Names of the documents retrieved for query {idx}: {', '.join(get_document_names(result))}\n")
