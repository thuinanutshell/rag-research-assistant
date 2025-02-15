#!/usr/bin/env python
# coding: utf-8

# # Data Crawling & Preprocessing

# In[40]:


from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin
import re
from cleantext import clean


# In[35]:


base_url = 'https://www.llamaindex.ai/blog'
response = requests.get(base_url)
html_doc = BeautifulSoup(response.content, 'html.parser')


# In[48]:


# Extract content for each blog, remove html tags/emojis and transform text into lowercase
def extract_content(url):
    r = requests.get(url)
    doc = BeautifulSoup(r.content, 'html.parser')
    content = doc.find('div', class_='BlogPost_htmlPost__Z5oDL')
    content = clean(content, no_emoji=True)
    content = content.lower()
    return content


# In[44]:


# Create a list of blogs
blogs = html_doc.find_all('div', class_='CardBlog_card__mm0Zw')
blog_list = []

for item in blogs:
    blog = {}
    blog['title'] = item.find('p', class_='CardBlog_title__qC51U').text.strip()
    blog['url'] = urljoin(base_url, item.find('a', href=True)['href'])
    blog['content'] = extract_content(blog['url'])
    blog_list.append(blog)


# In[47]:


with open('blogs.json', 'w') as file:
    json.dump(blog_list, file, indent=4)


# # Vector Embeddings & Vector Store

# In[52]:


from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core import Document


# In[62]:


from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding


# In[66]:


from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector


# In[53]:


with open('blogs.json', 'r') as file:
    data = json.load(file)


# In[57]:


# Create a list of documents with metadata
documents = [
    Document(
        text=item['content'].strip(),
        metadata={'title':item['title'], 'link':item['url']}
    ) for item in data if item['content'].strip()
]

print('The number of blog posts:', len(documents))


# In[59]:


# Split documents into nodes
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents) # Each document is split separately
print("The number of nodes:", len(nodes))


# In[64]:


# Load LLM Model
Settings.llm = Gemini(api_key=gemini_key, model='models/gemini-pro')
Settings.embed_model = GeminiEmbedding(api_key=gemini_key, model='models/embedding-001')
print('LLM model and embedding loaded')


# In[67]:


vector_index = VectorStoreIndex(nodes)


# # Retrieval & Generation

# In[70]:


from llama_index.core.query_engine import RetrieverQueryEngine


# In[75]:


retriever = vector_index.as_retriever(similarity_top_k=5)
query_engine = RetrieverQueryEngine.from_args(retriever)


# In[78]:


def get_response(query: str):
    response = query_engine.query(query)
    print(f"Query: {query}")
    print(f"Response: {response}")
    
    print("\nRelevant source information:")
    for node in response.source_nodes:
        print(f"- Content: {node.node.text[:100]}...")  # Print first 100 characters
        print(f"  Metadata: {node.node.metadata}")
        print(f"  Relevance Score: {node.score}")
        print("---")
    return response


# In[80]:


query = "What are the two main metrics used to evaluate the performance of the different rerankers in the RAG system?"
response = get_response(query)


# In[ ]:




