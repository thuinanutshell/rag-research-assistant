# Building A Chatbot Using Retrieval Augmented Generation (RAG)
<img width="1341" alt="Screenshot 2024-07-21 at 2 03 46 AM" src="https://github.com/user-attachments/assets/75afce4b-470e-46cb-87bf-8685851173fd">

## Overview
The chatbot can answer questions related to LlamaIndex's blog posts: https://www.llamaindex.ai/blog
* Learn how to crawl a large amount of data using Scrapy & BeautifulSoup
* Learn how to transform the data optimally
* Compare the performance of different LLM models

## Step 1: Planning
| Step | Objective | Library/Model |
| --- | --- | --- |
| 1 | Data Crawling | Scrapy or BeautifulSoup |
| 2 | Data Transformation (Vector-based) | Word2Vec, BERT, TF-IDF Vectorization (sklearn) |
| 3 | Choose an LLM model | OpenAI, Gemini, Claude, LlamaIndex |
| 4 | Retrieval Techniques & Query Engines | Elasticsearch |
| 5 | Optimization | Pinecone |
| 6 | Evaluation | Accuracy & Relevance |

## Step 2: Data Preparation
The goal is to crawl the data of 160 blog posts on the LlamaIndex website. Each blog post item should contain the URL, title, and content. The content consists of text, code, and figures/images. So, I need to make sure that I crawl sufficient content in different formats and preprocess them later.

## Step 3: Data Transformation
### Chunking
### Text Preprocessing
### Tokenization
### Vector Embeddings

## Step 4: Integrate LLM APIs

## Step 5: Optimization

## Step 6: Evaluation

## Key Learnings
- Always start small. I was struggling at first to understand the chunking part. It took me 2 days to process a large dataset of blog posts. When the dataset is large, you get overwhelmed easily. So I decided to play around with only one single blog post to understand the underlying mechanism of chunking. And it worked :) By breaking a big problem down into smaller pieces and go from there, everything is more manageable.
