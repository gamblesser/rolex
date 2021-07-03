import scrapy
import json
from scrapy.http import Request as Req


class RolexSpider(scrapy.Spider):
    name = 'rolex'
    allowed_domains = ['masbahrain.com','search.rolex.com']
    start_urls = ['http://masbahrain.com/']
    headers = {'Host': 'search.rolex.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Origin': 'https://corners.rolex.com',
'Connection': 'keep-alive',
'Referer': 'https://corners.rolex.com/',}
    
    def convent_to_json(self,resp):
        return json.loads(resp.body)['response']['docs']



    def parse(self, response):
        return Req('https://search.rolex.com/solr/2021/corners?fq=lang:en&fq=&start=0&rows=10000&facet=true',headers=self.headers,callback=self.parse_listOfWatches)


    def parse_listOfWatches(self,response):

        for watch in self.convent_to_json(response):
            yield Req(f'https://search.rolex.com/solr/2021/modelpage?q={watch["rmc"]}&fq=lang:en',headers=self.headers,callback=self.parse_watch)



    def parse_watch(self,response):
        watch_data = self.convent_to_json(response)[0]
        watch_labels = watch_data['dial']['labels']
        watch_movement= watch_data['movement']['labels']
        watch_case = watch_data['case']
        watch_dial = watch_data['dial']
        yield {
        'reference':watch_data['reference_code'],
        'modelCase':watch_case['labels']['title'],
        'bezel':watch_case['labels']['bezel'],
        'water_resistance':watch_case['labels']['water_resistance'],
        'movement':watch_movement['title'],
        'calibre':watch_movement['calibre'],
        'powerReserve':watch_movement['autonomy'],
        'bracelet':watch_case['labels']['title'],
        'dial':watch_dial['labels']['title'],
        'certification':watch_movement['certification'],
        }


