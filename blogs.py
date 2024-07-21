from pathlib import Path

import scrapy 

# Define attributes to the Spider
class BlogPosts(scrapy.Spider):
    name = 'blogs'
    start_urls = ["https://www.llamaindex.ai/blog"]

    def parse(self, response):
        blog_lists = []
        # Loop through all the blog cards on the page with the defined class
        # Extract the title and the href link using the get() method
        for blog in response.css('div.CardBlog_card__mm0Zw p'):
            title = blog.css('a::text').get()
            link = blog.css('a::attr(href)').get()

           # Return the list consisting of title and link
            if title is not None:
                blog_lists.append({
                    'title': title,
                    'link': response.urljoin(link) 
               })
        yield {'blogs': blog_lists}

        for blog in blog_lists:
            yield scrapy.Request(blog['link'], callback=self.parse_blog_content)
     
    def parse_blog_content(self, response):
        content = response.css("div.BlogPost_htmlPost__Z5oDL p::text").getall()
        yield {
            'url': response.url,
            'content': content
        }
