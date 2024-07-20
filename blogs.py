from pathlib import Path

import scrapy 

# Define some attributes to the Spider
class BlogPosts(scrapy.Spider):
    name = 'blogs'

    def start_requests(self):
        urls = [
            "https://www.llamaindex.ai/blog/improving-vector-search-reranking-with-postgresml-and-llamaindex",
            "https://www.llamaindex.ai/blog/introducing-llama-agents-a-powerful-framework-for-building-production-multi-agent-ai-systems"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"blog_posts-{page}.pdf"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")