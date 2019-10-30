import scrapy 
from urllib.parse import urljoin
from scrapy.http import Request
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html



class PycoderSpider(scrapy.Spider):
	name = "pycoder"
	start_urls = [
		'https://www.booking.com/searchresults.ru.html?label=gen173nr-1FCAQoggJCDWNpdHlfLTMyMTIyMTZIIVgEaIABiAEBmAEhuAEZyAEM2AEB6AEB-AECiAIBqAIDuAKn54ztBcACAQ&sid=8b14cb8fba2ad81fbb135734e26620ae&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.ru.html%3Flabel%3Dgen173nr-1FCAQoggJCDWNpdHlfLTMyMTIyMTZIIVgEaIABiAEBmAEhuAEZyAEM2AEB6AEB-AECiAIBqAIDuAKn54ztBcACAQ%3Bsid%3D8b14cb8fba2ad81fbb135734e26620ae%3Btmpl%3Dsearchresults%3Bcity%3D-3212216%3Bclass_interval%3D1%3Bdest_id%3D-3212216%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrpvid%3D4f046553c05601b1%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Btop_ufis%3D1%26%3B&ss=Рига&is_ski_area=0&ssne=Рига&ssne_untouched=Рига&city=-3212216&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&from_sf=1&rows=25'
	]
	visited_urls = []
	offset = 0
	rooms = []

	def parse(self, response):
			count = int(float (response.xpath('count(//a[@class="hotel_name_link url"]/@href)').extract()[0]))
			for post_link in response.xpath('//a[@class="hotel_name_link url"]/@href').getall():
				post_link = post_link.replace("\r","")
				post_link = post_link.replace("\n","")
				post_link = post_link.replace("\t","")
				url = urljoin(response.url , post_link)
				yield scrapy.Request(url,callback=self.parsehotel)
				print("	JOINED TO HOTEL:" + url)
				 
			print (count)
			if(count<=1):
				return

			self.offset += 25
			#&offset=
			next_page_url = self.start_urls[0] + "&offset=" + str(self.offset) 
			yield scrapy.Request(next_page_url,callback=self.parse)
		
	def parsehotel(self, response):
		for hotel in response.xpath('//a[@class="hotel_name_link url"]/@href').getall():
			hot = urljoin(response.hot , hotel)
			#for hot in response.xpath('//a[@class=""]/@text')
