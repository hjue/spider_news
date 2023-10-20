# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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
        content = f"""# {title}

{brief}
"""
        open(fileName,'w').write(content)
        print(fileName)
        return item
