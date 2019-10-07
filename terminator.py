import scrapy 
from urllib.parse import urljoin
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html

class HotelSpider(scrapy.Spider):
	name = "carl"
	#start_urls =  ["https://www.booking.com/searchresults.ru.html?aid=304142&label=gen173nr-1FCAQoggJCDWNpdHlfLTMyMTIyMTZIIVgEaIABiAEBmAEhuAEZyAEM2AEB6AEB-AECiAIBqAIDuALh7-DpBcACAQ&sid=8b14cb8fba2ad81fbb135734e26620ae&tmpl=searchresults&city=-3212216&class_interval=1&dest_id=-3212216&dest_type=city&dtdisc=0&inac=0&index_postcard=0&label_click=undef&order=popularity&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=0b187d6a447400ee&ss_all=0&ssb=empty&sshis=0&rows=15"]	


	def start_requests(self):
		yield scrapy.Request('https://www.booking.com/searchresults.ru.html?aid=304142&label=gen173nr-1FCAQoggJCDWNpdHlfLTMyMTIyMTZIIVgEaIABiAEBmAEhuAEZyAEM2AEB6AEB-AECiAIBqAIDuALh7-DpBcACAQ&sid=8b14cb8fba2ad81fbb135734e26620ae&tmpl=searchresults&city=-3212216&class_interval=1&dest_id=-3212216&dest_type=city&dtdisc=0&inac=0&index_postcard=0&label_click=undef&order=popularity&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=0b187d6a447400ee&ss_all=0&ssb=empty&sshis=0&rows=30', self.parse,
			meta={
			   'splash': {
				   'endpoint': 'render.html'
			   }
			}
		)



	def parse(self , response):
		for post_link in response.xpath('//a[@class="hotel_name_link url"]/@href').extract():
			post_link = post_link.replace("\r","")
			post_link = post_link.replace("\n","")
			post_link = post_link.replace("\t","")
			url = urljoin(response.url, post_link)
			print("post link to hotel "+ url)
			yield response.follow(url,self.parse_hotel)


		next_page_url = response.xpath("//a[@class='bui-pagination__link sr_pagination_link']/@href").extract_first()
		if next_page_url:
			next_href = next_page_url
			next_href = next_href.replace("\r","")
			next_href = next_href.replace("\n","")
			next_href = next_href.replace("\t","")
			print("next_page "+next_href)
			yield scrapy.Request(next_href,self.parse,
				meta={
			   'splash': {
				   'endpoint': 'render.html'
			   }
			})



	def parse_hotel(self, response):
		yield{
			"url":response.url
		}


