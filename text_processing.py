import re
import unicodedata
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('stopwords')

with open('input/blogs.json') as file:
    data = json.load(file)

"""
- lowercase
- remove stopwords
- remove punctuations
- remove special characters such as emojis
"""
stop_words = set(stopwords.words("english"))
pattern = r'[^a-zA-Z0-9\s]'
lowercase_data = [
   {'url': item['url'],
     'title': word_tokenize(re.sub(pattern, '', item['title']).lower()),
     'content': word_tokenize(re.sub(pattern, '', ''.join(item['content'])).lower())}
    for item in data
]

def remove_stopwords(data):
    cleaned_data = []
    for item in data:
       cleaned_item = {
           'url': item['url'],
           'title': [word for word in item['title'] if word not in stop_words],
           'content': [word for word in item['content'] if word not in stop_words]
       }
       cleaned_data.append(cleaned_item)
    return cleaned_data

cleaned_data = remove_stopwords(lowercase_data)

# Export the cleaned data into a JSON file
output_file = 'cleaned_text.json'

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

print(f"Data has been cleaned and saved to {output_file}")

