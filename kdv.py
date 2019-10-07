import scrapy 
from urllib.parse import urljoin
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html



class PycoderSpider(scrapy.Spider):
	name = "pycoder"
	start_urls = [
		'https://www.booking.com/searchresults.ru.html?label=gen173nr-1DCAQoggJCDWNpdHlfLTMyMTIyMTZIIVgEaIABiAEBmAEhuAEZyAEP2AED6AEB-AECiAIBqAIDuAKIwsjsBcACAQ&sid=7b7d32e62b0b16ad4055905d9054b0c3&tmpl=searchresults&city=-3212216&class_interval=1&dest_id=-3212216&dest_type=city&dtdisc=0&inac=0&index_postcard=0&label_click=undef&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=7ad66dc45a180039&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25',

	]
	visited_urls = []

	def parse(self, response):
			for post_link in response.xpath('//a[@class="hotel_name_link url"]/@href').getall():
				post_link = post_link.replace("\r","")
				post_link = post_link.replace("\n","")
				post_link = post_link.replace("\t","")
				url = urljoin(response.url , post_link)
				print("	JOINED TO HOTEL:" + url)
				#yield response.follow(post_link,callback=self.parse)   
				


			
			next_page_url = response.xpath("//a[@class='bui-pagination__link sr_pagination_link']/@href").extract()
			if next_page_url:
				next_href = next_page_url[-1]
				next_page_url = next_href
				next_page_url = next_page_url.replace("\r","")
				next_page_url = next_page_url.replace("\n","")
				next_page_url = next_page_url.replace("\t","")
				next_page_url = urljoin(response.url +'/',next_href)
				print("	NEXT_PAGE:"+next_page_url)
				yield scrapy.Request(next_page_url,callback=self.parse)
				