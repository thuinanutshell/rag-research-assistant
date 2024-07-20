from pathlib import Path

import scrapy 

class BlogPosts(scrapy.Spider):
    name = 'blogs'
    
    start_urls = [
        "https://www.llamaindex.ai/blog"
    ]
    
    def parse(self, response):
        for blog in response.css('div.CardBlog_card__mm0Zw p'):
            title = blog.css('a::text').get()
            link = blog.css('a::attr(href)').get()

            if title is not None:
                yield {
                    'title': title,
                    'link': link 
                }
