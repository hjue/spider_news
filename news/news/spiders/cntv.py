from typing import Any, Optional
import scrapy
import w3lib
import datetime
import re

class CntvSpider(scrapy.Spider):
    name = "cntv"
    allowed_domains = ["cntv.cn"]
    url = ''
    start_urls = []
    videos = []
    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        if hasattr(self, 'date'):
            print(self.date,'-'*30)
            strTime = datetime.datetime.strptime(self.date, "%Y-%m-%d" ).strftime("%Y%m%d")
        else:
            current_time = datetime.datetime.now().time()
            target_time = datetime.time(21, 0)  # 晚上9点的时间
            strTime = (datetime.date.today() + datetime.timedelta(-1)).strftime("%Y%m%d")
            if current_time > target_time:
                strTime = (datetime.date.today() ).strftime("%Y%m%d")                 
        
        self.url = f'https://tv.cctv.com/lm/xwlb/day/{strTime}.shtml'            
        self.start_urls = [self.url]
        
    
    def parse(self, response):

        url=response.css('li a::attr(href)')[1].get()
        lis = response.css('li')
        for li in lis:
            title=li.css('a')[0].attrib['title'].replace('[视频]','')
            link = li.css('a')[0].attrib['href']
            self.videos.append({'title':title,'url':link})
            

        yield scrapy.Request(url, callback=self.parseBrief, dont_filter=True)


    def parseBrief(self, response):

        brief = w3lib.html.remove_tags(response.css('.video_brief').get())
        lastLine = brief.split('\r\n')[-1]
        dateStr  = re.findall(r'\d{8}',lastLine)[0]
        newsDate = datetime.datetime(int(dateStr[0:4]), int(dateStr[4:6]), int(dateStr[6:8]))
        # 去掉第一行（'本期节目主要内容：）和最后一行（（《新闻联播》 20231018 19:00））的内容
        brief = '\n\n'.join(brief.split('\r\n')[1:-1])
        title = '%s 新闻联播主要内容' % newsDate.strftime("%Y年%m月%d日")
        yield {'brief':brief,'date':newsDate,'title':title,'url':self.url,'videos':self.videos}