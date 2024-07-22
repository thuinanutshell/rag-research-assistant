import re
from cleantext import clean
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('stopwords')

with open('input/content.json') as file:
    data = json.load(file)

# Text Preprocessing Before Chunking
"""
Preprocess the text data by:
- remove html tags
- transform to lowercase
- remove stopwords
- remove whitespae
- remove special characters such as emojis
"""

# Define patterns to remove from the text
html_tags = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
whitespace = re.compile(r'\s+')
stopwords = set(stopwords.words('english'))


def preprocess_text(text):
    for item in text:
        item['content'] = ' '.join(item['content'])
        item['content'] = re.sub(html_tags, '', item['content'])
        item['content'] = clean(item['content'], no_emoji=True)
        item['content'] = re.sub(whitespace,' ', item['content']).strip()
        item['content'] = item['content'].lower()
    return text

def remove_stopwords(text):
    for item in text:
        item['content'] = ' '.join([word for word in word_tokenize(item['content']) if word not in stopwords])
    return text

cleaned_data = preprocess_text(data)
cleaned_data = remove_stopwords(cleaned_data)

# Export the cleaned data into a JSON file
output_file = 'cleaned_text.json'

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)
