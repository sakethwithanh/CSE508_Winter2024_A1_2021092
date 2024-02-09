import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

nltk.download('punkt')
nltk.download('stopwords')

# preprocess
def preprocess_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()
     # a. Lowercase the text
    content = content.lower()
    # b. Tokenization
    tokens = word_tokenize(content)
    # c. Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # d. Remove punctuations
    tokens = [token for token in tokens if token not in string.punctuation]
    temp_tokens = []
    for token in tokens:
        temp_token = ""
        for char in token:
            if char.isalnum():
                temp_token += char
        temp_tokens.append(temp_token)
    tokens = temp_tokens
    # e. Remove blank space tokens
    tokens = [token for token in tokens if token.strip()]
    # Save the preprocessed content to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(tokens))
    return tokens

input_directory = r'D:\Studies\SEM6\\Information Retrieval\Assignments\CSE508_Winter2024_A1_2021092\\text_files'
output_directory = r'D:\Studies\SEM6\\Information Retrieval\Assignments\CSE508_Winter2024_A1_2021092\\processed_text_files'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
files = os.listdir(input_directory)

# Perform preprocessing steps on each file
for file_name in files:
    input_file_path = os.path.join(input_directory, file_name)
    output_file_path = os.path.join(output_directory, f"processed_{file_name}")
    preprocess_file(input_file_path, output_file_path)

for file in files[0:5]:
    file_path = "D:\\Studies\\SEM6\\Information Retrieval\\Assignments\\CSE508_Winter2024_A1_2021092\\text_files\\"  + file

    file_content = ""
    with open(file_path, 'r') as f:
        for line in f:
            file_content += line

    sample_file_path = "D:\\Studies\\SEM6\\Information Retrieval\\Assignments\\CSE508_Winter2024_A1_2021092\\sample_files\\" + file
    with open(sample_file_path, 'a') as f:
        f.write("Before Preprocessing: \n")
        for token in file_content.split():
            f.write(token + '\n')
        f.write("\n\n\n")
        
    #lowercase
    file_content = file_content.lower()

    with open(sample_file_path, 'a') as f:
        f.write("\n\nAfter Lowercasing:\n")
        for token in file_content.split():
            f.write(token + '\n')
        
        f.write('\n\n\n')

    # tornizer
    file_content = word_tokenize(file_content)
    with open(sample_file_path,'a') as f:
        f.write("\n\nAfter tokenizing :\n")
        for token in file_content:
            f.write(token + "\n ")
        f.write("\n\n\n")
# stopword
    stop_words = set(stopwords.words('english'))
    file_content = [token for token in file_content if token not in stop_words]
    with open(sample_file_path,'a') as f:
        f.write("\n\nAfter Stop Word:\n")
        for token in file_content:
            f.write(token + "\n")
        f.write("\n\n\n")
    # punctuation
    file_content = [token for token in file_content if token not in string.punctuation]
    temp_tokens = []

    for token in file_content:
        temp_token = ""
        for char in token:
            if char.isalnum():
                temp_token += char
        temp_tokens.append(temp_token)
    

    file_content = temp_tokens
    with open(sample_file_path,'a') as f:
        f.write("\n\nAfter punctuaion:\n")
        for token in file_content:
            f.write(token + "\n")
        f.write("\n\n\n")
    
     # e. Remove blank space tokens
    file_content  = [token for token in file_content if token.strip()]
    with open(sample_file_path,'a') as f:
        f.write("\n\nAfter removing blank space  :\n")
        for token in file_content:
            f.write(token + "\n ")
        f.write("\n\n\n")

    
        


    
