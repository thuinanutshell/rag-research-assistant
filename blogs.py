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

           # Add items to the blog_lists list
            if title is not None:
                blog_lists.append({
                    'title': title,
                    'link': response.urljoin(link) # convert to absolute urls
               })
        # Return a dictionary with the key 'blogs' and its value
        yield {'blogs': blog_lists}

        # Loop through each href link in the blog_lists and request from each blog link
        for blog in blog_lists:
            yield scrapy.Request(blog['link'], callback=self.parse_blog_content)

    # Create another function to get the content from each url 
    def parse_blog_content(self, response):
        content = response.css("div.BlogPost_htmlPost__Z5oDL p::text").getall()
        yield {
            'url': response.url,
            'content': content
        }
