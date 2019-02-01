#!/home/yao/anaconda3/bin/python

import scrapy
from scrapy.selector import Selector
import pickle
import datetime
import os
import webbrowser

class QuotesSpider(scrapy.Spider):
    name = "china"
    pickle_path = 'saved_items.p'




    def start_requests(self):
        BASE_URLs = ['https://www.ricardo.ch/de/c/antiquites-et-arts-38399/chinesisch', 
        			 'https://www.ricardo.ch/de/c/antiquitaeten-und-kunst-38399/asiatika', 
        			 'https://www.ricardo.ch/de/c/antiquitaeten-und-kunst-38399/japanisch',
        			 ]
        urls = [BASE_URL+'?page='+str(i) for i in range(1,30) for BASE_URL in BASE_URLs]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        saved_items = pickle.load(open(self.pickle_path, 'rb')) if os.path.exists(self.pickle_path) else dict()
        item_ids = Selector(response=response).xpath('//a[@class="ric-article"]/@data-ric-article-id').extract()
        item_urls = ['https://www.ricardo.ch' + item for item in Selector(response=response).xpath('//a[@class="ric-article"]/@href').extract()]
        item_image_urls = Selector(response=response).xpath('//a[@class="ric-article"]/div/div/img/@src').extract()

        vals = zip(item_urls, item_image_urls)
        new_pairs = dict(zip(item_ids, vals))

        new_items = list()
        for key, val in new_pairs.items():
            if key not in saved_items:
                new_items.append(val)
                webbrowser.open(val[0])
                saved_items[key] = val
                print(1)

        filename = 'china-'+datetime.datetime.today().strftime('%Y-%m-%d')+'.txt'
        with open(filename, 'a') as f:
            for k,v in new_items:
                f.write(k+'\t'+v+'\n')
        self.log('Saved file %s' % filename)

        pickle.dump(saved_items, open(self.pickle_path, 'wb'))