#!/usr/bin/env python
# coding: utf-8

# # Data Crawling

# In[14]:


from bs4 import BeautifulSoup
import requests
import json


# In[15]:


url = 'https://www.llamaindex.ai/blog/improving-vector-search-reranking-with-postgresml-and-llamaindex'
r = requests.get(url)
s = BeautifulSoup(r.content, 'html.parser')
p = s.find_all('p', class_='Text_text__zPO0D Text_text-size-16__PkjFu')

p_list = []
counter = 1
for item in p:
    content = {}
    if item.text.strip() and (item.next_sibling and item.next_sibling.name != 'pre'):
        content['content'] = item.text.strip()
        content['id'] = f'paragraph_{counter}'
        p_list.append(content)
        counter += 1


# # Data Preprocessing

# In[16]:


import re


# In[17]:


for item in p_list:
    item['content'] = item['content'].lower()


# In[18]:


p_list


# In[19]:


with open('sing_doc.json', 'w') as f:
    json.dump(p_list, f, indent=4)


# # Embeddings

# In[20]:


from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core import Document


# In[21]:


from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding


# In[22]:


from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector


# In[23]:


with open('sing_doc.json', 'r') as file:
    data = json.load(file)


# In[28]:


# Create documents with metadata, filtering out empty paragraphs
documents = [
    Document(
        text=item['content'].strip(), 
        metadata={"id": item['id']}
    ) 
    for item in data if item['content'].strip()  # Filter out empty paragraphs
]

print(len(documents))


# In[29]:


# Split documents into nodes
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents) # Each document is split separately
print("len of nodes:", len(nodes))


# In[30]:


# Load LLM Model
Settings.llm = Gemini(api_key=gemini_key, model='models/gemini-pro')
Settings.embed_model = GeminiEmbedding(api_key=gemini_key, model='models/embedding-001')
print('LLM model and embedding loaded')


# In[31]:


# Vector Store Index
summary_index = SummaryIndex(nodes)
vector_index = VectorStoreIndex(nodes)
print('Summary and Vector Index loaded')


# # Generation

# In[32]:


# Summary Query Engine
summary_query_engine = summary_index.as_query_engine(
    response_node="tree summarize",
    use_async=True
)


# In[33]:


# Vector Query Engine
vector_query_engine = vector_index.as_query_engine()

summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description="Useful for summarization questions related to any topic in Deep Learning paper"
)

vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for retrieving specific context from the Deep Learning paper."
)

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[summary_tool, vector_tool],
    verbose=True
)


# In[34]:


question1 = "What is the summary of the document?"
response1 = query_engine.query(question1)
print("Question 1:", question1)
print(str(response1))


# In[35]:


question2 = "What are the key points in the document? Which paragraph are you referring to?"
response2 = query_engine.query(question2)
print("Question 2:", question2)
print(str(response2))

