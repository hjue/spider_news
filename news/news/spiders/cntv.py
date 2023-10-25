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

    def parseBriefByBody(self, text):

        lines = text.split('\n')        
        lines = list(map(lambda x:x.strip(),lines))
        lastLine =lines[-1]
        
        dateStr  = re.findall(r'\d{8}',lastLine)[0]
        newsDate = datetime.datetime(int(dateStr[0:4]), int(dateStr[4:6]), int(dateStr[6:8]))            
        # 去掉第一行（'本期节目主要内容：）和最后一行（（《新闻联播》 20231018 19:00））的内容
        brief = '\n\n'.join(lines[1:-1])
        title = '%s 新闻联播主要内容' % newsDate.strftime("%Y年%m月%d日")
        return {'brief':brief,'date':newsDate,'title':title,'url':self.url,'videos':self.videos}

    def parseBriefByMeta(self, text):

        brief = text.replace('国内联播快讯：','国内联播快讯：\n\n').replace('国际联播快讯：','国际联播快讯：\n\n')
        lines = brief.split('；')
        if lines[0].split('主要内容：')==2:
            lines[0] = lines[0].split('主要内容：')[1].strip()

        lastLine = lines[-1]
        dateStr  = re.findall(r'\d{8}',lastLine)[0]
        newsDate = datetime.datetime(int(dateStr[0:4]), int(dateStr[4:6]), int(dateStr[6:8]))

        lastLine = re.sub(r'（《新闻联播》\s+\d{8}\s+[\d:]+）','',lastLine).strip()
        lines[-1] = lastLine

        lines = list(map(lambda x:x.strip(),lines))

        brief = '\n\n'.join(lines)
        title = '%s 新闻联播主要内容' % newsDate.strftime("%Y年%m月%d日")
        
        return {'brief':brief,'date':newsDate,'title':title,'url':self.url,'videos':self.videos}

        
        # raise scrapy.exceptions.CloseSpider('未找到需要的内容') 
            
    def parseBrief(self, response):

        brief = response.css('meta[name="description"]::attr(content)').get()
        if brief.count('；')>5:
            yield self.parseBriefByMeta(brief)
        else:
            brief = w3lib.html.remove_tags(response.css('.video_brief').get())
            yield self.parseBriefByBody(brief)

        