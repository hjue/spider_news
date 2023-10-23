# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
import os
import json
import datetime

class NewsPipeline:
    def process_item(self, item, spider):
        return item


class SavingToArtifacts(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        fileName = f'../artifacts/xwlb-{item["date"].strftime("%Y-%m-%d")}.md'
        title = item['title']
        brief = item['brief']
        url = item['url']
        content = f"""# [{title}]({url})

{brief}

## 视频

"""
        for video in item['videos']:
            content += f'[{video["title"]}]({video["url"]})'+'\n\n'

        content += f'[视频地址]({url}) \n\n'
        open(fileName,'w').write(content)
        print(fileName)
        return item



class PushToMobile(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        title = item['title']
        brief = item['brief']
        date = item['date']
        url = item['url']

        deviceKey=os.getenv('DEVICEKEY')
        apiUrl = f'https://api.day.app/push'
        headers = {'Content-Type': 'application/json'}
        body = f"""{title}

{brief}

视频地址: {url}

"""
        data = {'title': title, 'body': body,
                'isArchive':1,"device_key": deviceKey}

        response = requests.post(apiUrl, headers=headers, data=json.dumps(data))
        print(response.status_code)
        print(response.text)
