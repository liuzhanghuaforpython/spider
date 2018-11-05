# -*- coding: utf-8 -*-
import scrapy

from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0
    allowed_domains = ['wz.sun0769.com']
    start_urls = [url+str(offset)]

    def parse(self, response):

        # 取出每个页面里帖子链接列表
        links=response.xpath("//div[@class='greyframe']/table//td/a[@class='news14']/@href")
        # 迭代发送每个帖子的请求，调用parse_item方法处理
        for link in links:
            link=link.extract()
            #print(link)
            yield scrapy.Request(url=link, callback=self.parse_item)
            # 设置页码终止条件，并且每次发送新的页面请求调用parse方法处理
            self.offset += 30
            if self.offset <= 96990:
                 yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    # 处理每个帖子里

    def parse_item(self, response):
        item = YangguangItem()
        # 标题
        item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract_first()
        # 编号
        item['number'] = item['title'].split(' ')[-1].split(":")[-1]
        # 文字内容，默认先取出有图片情况下的文字内容列表
        content = response.xpath('//div[@class="contentext"]/text()').extract_first()
        # 如果没有内容，则取出没有图片情况下的文字内容列表
        if not content:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract_first()
            # content为列表，通过join方法拼接为字符串，并去除首尾空格
            item['content'] = content
        else:
            item['content'] = content
        # 链接
        item['url'] = response.url

        yield item

