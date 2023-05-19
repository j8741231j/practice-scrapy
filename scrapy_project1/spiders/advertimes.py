import scrapy

class AdvertimesSpider(scrapy.Spider):
    name = "advertimes"
    allowed_domains = ["www.advertimes.com"]
    start_urls = ["https://www.advertimes.com"]

    def parse(self, response):
        articles = response.xpath('//ul[@class="col-article-list"]/li')
        for article in articles:
            link = article.xpath(".//a/@href").get()
            title = article.xpath('.//a/h3[@class="col-article-list-tit"]/text()').get()
            update_date = article.xpath('.//a/div[@class="meta-bottom"]//span[@class="update-date"]/text()').get()
            # yield scrapy.Request(url=response.urljoin(link))
            yield response.follow(url=link, callback=self.parse_page,meta={'title':title,"update_date":update_date})

    def parse_page(self, response):
        # 在這裡對跟隨連結的回應進行處理
        title = response.request.meta['title']
        update_date = response.request.meta['update_date']
        articles = response.xpath('//div[@class="entry-txt"]')
        for article in articles:
            paragraph= article.xpath('.//p/text()').getall()
            yield {
                'title': title,
                'update_date':update_date,
                'paragraph':paragraph
            }



   
